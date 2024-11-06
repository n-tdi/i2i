from bluepy.btle import Peripheral, DefaultDelegate, BTLEDisconnectError, Scanner
import struct
import subprocess
import time

class NotificationDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)
        self.last_value = None  # Store the last received value

    def handleNotification(self, cHandle, data):
        # Decode the incoming data from the ESP32
        value = data.decode('utf-8')

        # Only process if the value is different from the last one
        if value != self.last_value:
            self.last_value = value  # Update the last value
    
    def getTokenized(self):
        return self.last_value.split()

class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

class Button():
    def __init__(self, id: int, func):
        self.id = id
        self.pressed: bool  = False
        self.func = func
    
    def press(self):
        self.pressed = True
    
    def release(self):
        self.pressed = False

    def onPress(self):
        return self.func(self) if self.pressed else None
    
def button1Pressed(button: Button):
    print("Button 1 pressed " + str(button.id))
    return None

def button2Pressed(button: Button):
    print("Button 2 pressed " + str(button.id))
    return None

class Buttons():
    def __init__(self, notificationDelegate: NotificationDelegate):
        self.notificationDelegate = notificationDelegate
        self.buttons = []
    def addButton(self, button: Button):
        self.buttons.append(button)

buttons = Buttons(NotificationDelegate())

devices = []

def startClient():
    esp32_addr = None

    while True:
        while True:
            # try:
            print("Starting BLE scanner...")
            scanner = Scanner().withDelegate(ScanDelegate())
            scanner.scan(0.5)
            devices = scanner.scan(8.0)
            break
            # except:
            #     print("Error: Unable to start scanner, restarting bluetooth...")
            #     subprocess.run(["systemctl", "restart", "bluetooth"]) 
            #     time.sleep(3)
            #     continue
        for dev in devices:
            for (adtype, desc, value) in dev.getScanData():
                if desc == "Complete Local Name" and value == "ESP32_BLE":
                    print(f"Device {dev.addr} ({dev.addrType}), RSSI={dev.rssi} dB")
                    print(f"  {desc} = {value}")
                    esp32_addr = dev.addr
                    break
            if (esp32_addr != None):
                break

        if esp32_addr is None:
            print("ESP32 not found!")
            time.sleep(1)
            continue
        else:
            print("ESP32 found!")
            break

    attempts = 0

    while True:
        try:
            # Create a Peripheral object
            esp32 = Peripheral(esp32_addr)

            # Set the delegate to handle notifications
            notification = NotificationDelegate()
            esp32.setDelegate(notification)

            # Discover services and characteristics
            esp32.writeCharacteristic(0x0011, struct.pack('<bb', 0x01, 0x00))  # Enable notifications (this might vary based on characteristic handle)

            print("Connected to ESP32. Waiting for notifications...")
            attempts = 0

            while True:
                if esp32.waitForNotifications(1.0):
                    # Handle received notifications
                    token = notification.getTokenized()
                    print(token)

                    for button in buttons.buttons:
                        if button.id == int(token[1]):
                            if token[2] == "Pressed":
                                button.press()
                            else:
                                button.release()
                            button.onPress()
                            break
                    continue

                

        except BTLEDisconnectError:
            if attempts >= 50:
                print("Failed to reconnect after 50 attempts. Exiting...")
                break
            print("Disconnected from ESP32")
            print("Reconnecting...")
            attempts += 1
