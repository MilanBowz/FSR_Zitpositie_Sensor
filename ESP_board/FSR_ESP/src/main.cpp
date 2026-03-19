#include <Arduino.h>

// Eenvoudige FSR uitlezing voor ESP32
// Aansluiting: FSR tussen 3.3V en GPIO34, met 10k pull-down weerstand naar GND.

#define FSR_PIN 34          // Gebruik GPIO34 (ADC1_CH6)

// Variabelen voor ruisfiltering (optioneel, maar aanbevolen)
const int numReadings = 10;  // Aantal samples voor middeling
int readings[numReadings];   // Array om samples op te slaan
int readIndex = 0;           // Huidige index in de array
int total = 0;               // Som van alle samples
int average = 0;             // Gemiddelde waarde

void setup() {
  Serial.begin(9600);      // Start seriële communicatie
  delay(1000);               // Korte wachttijd voor stabilisatie

  // Configureer ADC voor ESP32 voor optimaal bereik (0 - 3.3V)
  analogReadResolution(12);  // 12-bit resolutie (0-4095)
  analogSetAttenuation(ADC_11db);  // Meetbereik 0-3.3V

  // Initialiseer de array voor het filter
  for (int i = 0; i < numReadings; i++) {
    readings[i] = 0;
  }

  Serial.println("FSR Sensor gestart - Druk op de sensor...");
  Serial.println("Raw Value,Spanning (V)"); // Header voor CSV
}

void loop() {
  // --- 1. Lees de ruwe ADC waarde ---
  int rawValue = analogRead(FSR_PIN);

  // --- 2. Eenvoudig voortschrijdend gemiddelde filter (verwijdert ruis) ---
  total = total - readings[readIndex];       // Verwijder oude waarde uit som
  readings[readIndex] = rawValue;            // Sla nieuwe waarde op
  total = total + readings[readIndex];       // Voeg nieuwe waarde toe aan som
  readIndex = (readIndex + 1) % numReadings; // Ga naar volgende index (circulair)

  average = total / numReadings;             // Bereken gemiddelde

  // --- 3. Converteer naar spanning (0 - 3.3V) ---
  //    Bij 12-bit (4095) = 3.3V
  float voltage = (average / 4095.0) * 3.3;

  // --- 4. Toon resultaten in Seriële Monitor ---
  //    Je kunt ook 'rawValue' gebruiken i.p.v. 'average' voor ongefiltreerde data
  Serial.print(average);
  Serial.print(",");
  Serial.println(voltage, 3); // 3 decimalen voor spanning

  // Kleine vertraging voor leesbaarheid (50ms = 20 samples per seconde)
  delay(50);
}