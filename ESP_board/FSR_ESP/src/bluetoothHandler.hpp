#ifndef BLUETOOTH_HANDLER_HPP
#define BLUETOOTH_HANDLER_HPP

#include <Arduino.h>
#include <BluetoothSerial.h>

class BluetoothHandler {
private:
    BluetoothSerial SerialBT;
    String deviceName;
    bool connected;
    unsigned long lastSendTime;
    int sendInterval; // milliseconden tussen verzendingen
    
    // Statistieken
    unsigned long packetsSent;
    unsigned long packetsFailed;
    
    void log(const String& message);
    
public:
    BluetoothHandler(const String& name = "ESP32_FSR_Sensor");
    ~BluetoothHandler();
    
    // Initialisatie en connectie
    bool begin();
    void end();
    bool isConnected();
    
    // Data verzenden
    bool sendData(const String& data);
    bool sendSensorData(int averageValue, float voltage);
    
    // Configuratie
    void setSendInterval(int intervalMs);
    void printStatus();
    
    // Update functie voor in loop()
    void update();
    
    // Getters voor statistieken
    unsigned long getPacketsSent() const { return packetsSent; }
    unsigned long getPacketsFailed() const { return packetsFailed; }
};

#endif // BLUETOOTH_HANDLER_HPP