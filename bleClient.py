from bluepy.btle import Peripheral, UUID
from bluepy.btle import Scanner, DefaultDelegate
import time

class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

scanner = Scanner().withDelegate(ScanDelegate())
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

print(f"Connecting to ESP32 ({esp32_addr})...")
esp32 = Peripheral(esp32_addr)

# The service and characteristic UUIDs should match those in the ESP32 code
service_uuid = UUID("4fafc201-1fb5-459e-8fcc-c5c9c331914b")
characteristic_uuid = UUID("beb5483e-36e1-4688-b7f5-ea07361b26a8")

service = esp32.getServiceByUUID(service_uuid)
characteristic = service.getCharacteristics(characteristic_uuid)[0]

esp32.writeCharacteristic(characteristic.getHandle() + 1, b"\x01\x00")

# Read from the ESP32 characteristic
initial_read = characteristic.read().decode('utf-8')
print(f"Initial read from ESP32: {initial_read}")

# Loop to listen for messages continuously
while True:
    value = characteristic.read().decode('utf-8')
    print(f"Received from ESP32: {value}")
    
    time.sleep(0.25)  # Add a delay to reduce CPU usage

