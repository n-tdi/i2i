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

// Callbacks for BLE server connection/disconnection
class MyCallbacks : public BLEServerCallbacks {
    void onConnect(BLEServer* pServer) {
      deviceConnected = true;
      Serial.println("Client connected");
      pCharacteristic->setValue("Connected");
      pCharacteristic->notify();
    }

    void onDisconnect(BLEServer* pServer) {
      deviceConnected = false;
      Serial.println("Client disconnected");
      pServer->startAdvertising();  // Start advertising again after disconnect
      Serial.println("Started advertising again");
    }
};

// Callbacks for characteristic write events
class MyCharacteristicCallbacks : public BLECharacteristicCallbacks {
    void onWrite(BLECharacteristic *pCharacteristic) {
      rxValue = pCharacteristic->getValue().c_str();  // Get the value sent from the Pi
      if (rxValue.length() > 0) {
        Serial.print("Received from Pi: ");
        Serial.println(rxValue);
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
                      BLECharacteristic::PROPERTY_WRITE |
                      BLECharacteristic::PROPERTY_NOTIFY
                    );

  pCharacteristic->setCallbacks(new MyCharacteristicCallbacks());

  // Start the service
  pService->start();

  // Start advertising
  BLEAdvertising *pAdvertising = BLEDevice::getAdvertising();
  pAdvertising->start();
  Serial.println("Waiting for a client connection...");
}

bool button1Pressed = false;
bool button2Pressed = false;

void loop() {
  // Check button states
  if (deviceConnected) {
    // Button 1 pressed
    if (digitalRead(BUTTON_1_PIN) == LOW && !button1Pressed) {
      button1Pressed = true;
      pCharacteristic->setValue("Button 1 Pressed");
      pCharacteristic->notify();  // Notify Raspberry Pi
      Serial.println("Button 1 Pressed");
    } 
    else if (digitalRead(BUTTON_1_PIN) == HIGH && button1Pressed) {
      button1Pressed = false;
      pCharacteristic->setValue("Button 1 Released");
      pCharacteristic->notify();  // Notify Raspberry Pi
      Serial.println("Button 1 Released");
    }

    // Button 2 pressed
    if (digitalRead(BUTTON_2_PIN) == LOW && !button2Pressed) {
      button2Pressed = true;
      pCharacteristic->setValue("Button 2 Pressed");
      pCharacteristic->notify();  // Notify Raspberry Pi
      Serial.println("Button 2 Pressed");
    } 
    else if (digitalRead(BUTTON_2_PIN) == HIGH && button2Pressed) {
      button2Pressed = false;
      pCharacteristic->setValue("Button 2 Released");
      pCharacteristic->notify();  // Notify Raspberry Pi
      Serial.println("Button 2 Released");
    }
  }
}
