from bluepy.btle import Peripheral, DefaultDelegate, BTLEDisconnectError, Scanner
import struct

class NotificationDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)
        self.last_value = None  # Store the last received value

    def handleNotification(self, cHandle, data):
        # Decode the incoming data from the ESP32
        value = data.decode('utf-8')

        # Only process if the value is different from the last one
        if value != self.last_value:
            print(f"Received new value: {value}")
            self.last_value = value  # Update the last value

class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

try:
  scanner = Scanner().withDelegate(ScanDelegate())
except:
  print("Error: Unable to start scanner, restart bluetooth?")
  exit(1)

devices = scanner.scan(7.0)

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

try:
    # Create a Peripheral object
    esp32 = Peripheral(esp32_addr)

    # Set the delegate to handle notifications
    esp32.setDelegate(NotificationDelegate())

    # Discover services and characteristics
    esp32.writeCharacteristic(0x0011, struct.pack('<bb', 0x01, 0x00))  # Enable notifications (this might vary based on characteristic handle)

    print("Connected to ESP32. Waiting for notifications...")

    while True:
        if esp32.waitForNotifications(1.0):
            # Handle received notifications
            continue

        

except BTLEDisconnectError:
    print("Disconnected from ESP32")
