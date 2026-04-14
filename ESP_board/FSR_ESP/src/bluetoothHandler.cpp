#include "BluetoothHandler.hpp"

BluetoothHandler::BluetoothHandler(const String& name)
    : deviceName(name)
    , connected(false)
    , lastSendTime(0)
    , sendInterval(100)  // Default: send every 100ms
    , packetsSent(0)
    , packetsFailed(0)
{
}

BluetoothHandler::~BluetoothHandler() {
    end();
}

void BluetoothHandler::log(const String& message) {
    Serial.println("[BT] " + message);
}

bool BluetoothHandler::begin() {
    // Initialize Serial for debugging
    // Serial.begin(9600);
    bool success = SerialBT.begin(deviceName);
    
    // Initialize Bluetooth
    log("Initializing Bluetooth...");
    
    if (success) {
        log("Bluetooth initialized successfully as: " + deviceName);
        log("Device is discoverable and ready for connections");
        connected = false;  // Start disconnected, wait for client
    } else {
        log("ERROR: Failed to initialize Bluetooth!");
    }
    
    return success;
}

void BluetoothHandler::end() {
    if (SerialBT.connected()) {
        SerialBT.disconnect();
    }
    SerialBT.end();
    log("Bluetooth stopped");
}

bool BluetoothHandler::isConnected() {
    connected = SerialBT.connected();
    return connected;
}

bool BluetoothHandler::sendData(const String& data) {
    if (!isConnected()) {
        packetsFailed++;
        return false;
    }
    
    // Send data with newline terminator
    size_t bytesSent = SerialBT.println(data);
    
    if (bytesSent > 0) {
        packetsSent++;
        log("Sent: " + data);
        return true;
    } else {
        packetsFailed++;
        log("ERROR: Failed to send data");
        return false;
    }
}

bool BluetoothHandler::sendSensorData(int rawValue, float averageValue) {
    // Format: "AVG:value avg of 10,RAW:value"
    String data = "AVG:" + String(averageValue) + ",RAW:" + String(rawValue);
    if(isConnected()){
        log("CONNECTED: " + data);
        return sendData(data);
    }
    else{
        log("NOT CONNECTED: " + data);
    }
    return false;
}

void BluetoothHandler::setSendInterval(int intervalMs) {
    sendInterval = intervalMs;
    log("Send interval set to " + String(intervalMs) + "ms");
}

void BluetoothHandler::printStatus() {
    log("=== Bluetooth Status ===");
    log("Device Name: " + deviceName);
    log("Connected: " + String(isConnected() ? "YES" : "NO"));
    log("Send Interval: " + String(sendInterval) + "ms");
    log("Packets Sent: " + String(packetsSent));
    log("Packets Failed: " + String(packetsFailed));
    if (packetsSent > 0) {
        float successRate = (float)packetsSent / (packetsSent + packetsFailed) * 100;
        log("Success Rate: " + String(successRate, 1) + "%");
    }
    log("========================");
}

void BluetoothHandler::update() {
    // Check connection status
    bool currentConnection = SerialBT.connected();
    
    if (currentConnection != connected) {
        connected = currentConnection;
        if (connected) {
            log("Client connected!");
        } else {
            log("Client disconnected");
        }
    }
}