#include <BLEDevice.h>
#include <BLEUtils.h>
#include <BLEServer.h>

#define BUTTON_1_PIN 20 // GPIO pin for Button 1
#define BUTTON_2_PIN 21 // GPIO pin for Button 2

#define SERVICE_UUID        "4fafc201-1fb5-459e-8fcc-c5c9c331914b"  // Custom service UUID
#define CHARACTERISTIC_UUID "beb5483e-36e1-4688-b7f5-ea07361b26a8"  // Custom characteristic UUID

BLECharacteristic *pCharacteristic;
bool deviceConnected = false;
String rxValue;  // Variable to store received data

class MyCallbacks : public BLEServerCallbacks {
    void onConnect(BLEServer* pServer) {
      deviceConnected = true;
    }

    void onDisconnect(BLEServer* pServer) {
      deviceConnected = false;
      pServer->startAdvertising();
      Serial.println("Started advertising again");
    }
};

class MyCharacteristicCallbacks : public BLECharacteristicCallbacks {
    void onWrite(BLECharacteristic *pCharacteristic) {
      rxValue = pCharacteristic->getValue();
      if (rxValue.length() > 0) {
        Serial.print("Received from Pi: ");
        Serial.println(rxValue.c_str());
      }
    }
};

void setup() {
  Serial.begin(115200);

  // Initialize buttons
  pinMode(BUTTON_1_PIN, INPUT_PULLUP); // Button 1
  pinMode(BUTTON_2_PIN, INPUT_PULLUP); // Button 2

  // Create the BLE Device
  BLEDevice::init("ESP32_BLE");

  // Create the BLE Server
  BLEServer *pServer = BLEDevice::createServer();
  pServer->setCallbacks(new MyCallbacks());

  // Create the BLE Service
  BLEService *pService = pServer->createService(SERVICE_UUID);

  // Create a BLE Characteristic
  pCharacteristic = pService->createCharacteristic(
                      CHARACTERISTIC_UUID,
                      BLECharacteristic::PROPERTY_READ |
                      BLECharacteristic::PROPERTY_WRITE
                    );

  pCharacteristic->setCallbacks(new MyCharacteristicCallbacks());

  // Start the service
  pService->start();

  // Start advertising
  BLEAdvertising *pAdvertising = BLEDevice::getAdvertising();
  pAdvertising->start();
  Serial.println("Waiting for a client connection...");
}

void loop() {
  // Check button states
  if (deviceConnected) {
    // Button 1 pressed
    if (digitalRead(BUTTON_1_PIN) == LOW) {
      pCharacteristic->setValue("Button 1 Pressed");
      pCharacteristic->notify();  // Notify Raspberry Pi
      Serial.println("Button 1 Pressed");
      delay(500);  // Debounce delay
    }

    // Button 2 pressed
    if (digitalRead(BUTTON_2_PIN) == LOW) {
      pCharacteristic->setValue("Button 2 Pressed");
      pCharacteristic->notify();  // Notify Raspberry Pi
      Serial.println("Button 2 Pressed");
      delay(500);  // Debounce delay
    }
  }
}
