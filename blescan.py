from bluepy.btle import Scanner, DefaultDelegate

class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            print(f"Discovered device: {dev.addr}")
        elif isNewData:
            print(f"Received new data from: {dev.addr}")

# Initialize the scanner
scanner = Scanner().withDelegate(ScanDelegate())
devices = scanner.scan(10.0)  # Scan for 10 seconds

for dev in devices:
    print(f"Device {dev.addr} (RSSI={dev.rssi}):")
    for (adtype, desc, value) in dev.getScanData():
        print(f"  {desc} = {value}")

