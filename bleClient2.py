from bluepy.btle import Peripheral, DefaultDelegate, BTLEDisconnectError
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

# ESP32 BLE address (replace with your device's address)
esp32_addr = "e8:06:90:67:15:6e"

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

        print("Waiting...")

except BTLEDisconnectError:
    print("Disconnected from ESP32")
