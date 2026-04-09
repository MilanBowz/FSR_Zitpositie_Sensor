#include <Arduino.h>
#include "bluetoothHandler.hpp"

// Eenvoudige FSR uitlezing voor ESP32
// Aansluiting: FSR tussen 3.3V en GPIO34, met 10k pull-down weerstand naar GND.

#define FSR_PIN 34          // Gebruik GPIO34/D34 (ADC1_CH6)

// Variabelen voor ruisfiltering
const int numReadings = 10;  // Aantal samples voor middeling
int readings[numReadings];   // Array om samples op te slaan
int readIndex = 0;           // Huidige index in de array
int total = 0;               // Som van alle samples
int average = 0;             // Gemiddelde waarde

// Bluetooth handler
BluetoothHandler bluetooth("ESP32_FSR_Sensor");

// Timing variabelen
unsigned long lastSensorRead = 0;
const int sensorReadInterval = 50; // 50ms = 20Hz

void setup() {
  bluetooth.begin();
  bluetooth.setSendInterval(50);

  // Configureer ADC voor ESP32 voor optimaal bereik (0 - 3.3V)
  analogReadResolution(12);  // 12-bit resolutie (0-4095)
  analogSetAttenuation(ADC_11db);  // Meetbereik 0-3.3V

  // Initialiseer de array voor het filter
  for (int i = 0; i < numReadings; i++) {
    readings[i] = 0;
  }

  bluetooth.printStatus();
}

void loop() {
    // Update Bluetooth status en verwerk inkomende commando's
    bluetooth.update();
    
    // Lees sensor met vaste interval
    if (millis() - lastSensorRead >= sensorReadInterval) {
        lastSensorRead = millis();
        
        // Lees raw ADC waarde
        int rawValue = analogRead(FSR_PIN);
        
        // Voortschrijdend gemiddelde filter
        total = total - readings[readIndex];
        readings[readIndex] = rawValue;
        total = total + readings[readIndex];
        readIndex = (readIndex + 1) % numReadings;
        average = total / numReadings;
        
        // Converteer naar spanning
        float voltage = (average / 4095.0) * 3.3;
        
        // Verstuur via Bluetooth als verbonden
        bluetooth.sendSensorData(average, voltage);
    }
    // delay(1);
}