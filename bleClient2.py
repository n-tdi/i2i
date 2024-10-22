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
    def __init__(self, id, func):
        self.id = id
        self.pressed = False
        self.func = func
    
    def press(self):
        self.pressed = True
    
    def release(self):
        self.pressed = False

    def onPress(self):
        return self.func(self) if self.pressed else None
    
def button1Pressed(button):
    print("Button 1 pressed " + str(button.id))
    return None

def button2Pressed(button):
    print("Button 2 pressed " + str(button.id))
    return None

class Buttons():
    def __init__(self, notificationDelegate):
        self.notificationDelegate = notificationDelegate
        self.buttons = [Button(1, button1Pressed), Button(2, button2Pressed)]

buttons = Buttons(NotificationDelegate())

devices = []

while True:
    try:
        print("Starting BLE scanner...")
        scanner = Scanner().withDelegate(ScanDelegate())
        devices = scanner.scan(4.0)
        break
    except:
        print("Error: Unable to start scanner, restarting bluetooth...")
        subprocess.run(["systemctl", "restart", "bluetooth"]) 
        time.sleep(3)
        continue


esp32_addr = None

for dev in devices:
    print(f"Device {dev.addr} ({dev.addrType}), RSSI={dev.rssi} dB")
    for (adtype, desc, value) in dev.getScanData():
        print(f"  {desc} = {value}")
        if desc == "Complete Local Name" and value == "ESP32_BLE":
            esp32_addr = dev.addr

if esp32_addr is None:
    print("ESP32 not found!")
    exit(1)


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

        while True:
            if esp32.waitForNotifications(1.0):
                # Handle received notifications
                token = notification.getTokenized()

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
        print("Disconnected from ESP32")
        print("Reconnecting...")
