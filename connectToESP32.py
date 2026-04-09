# serial_ble_client.py
import serial
import serial.tools.list_ports
import time
import sys

# CONFIGURATION - CHANGE THIS TO YOUR COM PORT
COM_PORT = "COM18"  # Replace with your COM port from Device Manager
BAUD_RATE = 9600   # Must match Serial.begin(9600) in your ESP32 code

def find_esp32_com_port():
    """Automatically find ESP32 Bluetooth COM port"""
    print("Searching for ESP32 Bluetooth COM port...")
    ports = serial.tools.list_ports.comports()
    
    for port in ports:
        # Look for Bluetooth SPP ports
        if "Bluetooth" in port.description or "Standard Serial" in port.description:
            print(f"  Found potential port: {port.device} - {port.description}")
            # You can try to connect to each one
            return port.device
    
    return None

def connect_and_read():
    """Connect to ESP32 via Bluetooth SPP and read data"""
    
    # Try to auto-find COM port if not specified
    port_to_use = COM_PORT
    if port_to_use == "COM3":  # Still default, try to auto-detect
        auto_port = find_esp32_com_port()
        if auto_port:
            port_to_use = auto_port
            print(f"Auto-detected COM port: {port_to_use}")
        else:
            print("Could not auto-detect ESP32 COM port")
            print(f"Using manual setting: {port_to_use}")
    
    print(f"\n{'='*50}")
    print(f"ESP32 Bluetooth SPP Client")
    print(f"COM Port: {port_to_use}")
    print(f"Baud Rate: {BAUD_RATE}")
    print(f"{'='*50}\n")
    
    try:
        # Open serial connection
        print(f"Connecting to {port_to_use}...")
        ser = serial.Serial(
            port=port_to_use,
            baudrate=BAUD_RATE,
            timeout=1,  # 1 second timeout
            write_timeout=1
        )
        
        print(f"✓ Connected to ESP32!\n")
        print("Waiting for data... (Press Ctrl+C to stop)\n")
        print("-" * 50)
        
        # Optional: Send a command to ESP32 (uncomment if needed)
        # ser.write(b"STATUS\n")
        
        packet_count = 0
        last_print_time = time.time()
        
        while True:
            # Read data from ESP32
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8', errors='ignore').strip()
                
                if line:
                    packet_count += 1
                    print(f"[{packet_count:4d}] {line}")
                    
                    # Parse the data (optional)
                    if "AVG:" in line and "VOLT:" in line:
                        # Extract values
                        try:
                            avg_part = line.split(',')[0].split(':')[1]
                            volt_part = line.split(',')[1].split(':')[1]
                            print(f"        → Average: {avg_part}, Voltage: {volt_part}V")
                        except:
                            pass
                
                # Print status every 5 seconds
                current_time = time.time()
                if current_time - last_print_time >= 5:
                    print(f"\n[STATUS] Packets received: {packet_count}")
                    print("-" * 50)
                    last_print_time = current_time
            
            # Small delay to prevent CPU hogging
            time.sleep(0.01)
            
    except serial.SerialException as e:
        print(f"\n❌ ERROR: Could not open {port_to_use}")
        print(f"   Details: {e}")
        print("\nTroubleshooting:")
        print("  1. Make sure ESP32 is paired with Windows")
        print("  2. Check the COM port number in Device Manager")
        print("  3. Close any other program using this COM port")
        print("  4. Try unplugging/repairing the ESP32")
        return False
        
    except KeyboardInterrupt:
        print("\n\n✓ Stopped by user")
        return True
        
    finally:
        if 'ser' in locals() and ser.is_open:
            ser.close()
            print("Serial connection closed")
    
    return True

def test_connection():
    """Quick test to verify COM port works"""
    import serial
    
    try:
        ser = serial.Serial(COM_PORT, BAUD_RATE, timeout=2)
        print(f"✓ Successfully opened {COM_PORT}")
        ser.close()
        return True
    except Exception as e:
        print(f"❌ Cannot open {COM_PORT}: {e}")
        return False

if __name__ == "__main__":
    # First, test if we can open the COM port
    print("ESP32 Bluetooth SPP Client for Windows 11")
    print("=" * 50)
    
    # Optional: List all COM ports
    print("\nAvailable COM ports:")
    ports = serial.tools.list_ports.comports()
    for port in ports:
        print(f"  {port.device}: {port.description}")
    
    print("\n" + "=" * 50)
    
    # Run the main connection
    success = connect_and_read()
    
    if not success:
        print("\nTroubleshooting Guide:")
        print("=====================")
        print("1. Open 'Bluetooth & devices' in Windows Settings")
        print("2. Click 'More devices and printer settings' (scroll down)")
        print("3. Click 'Add a device' and pair with 'ESP32_FSR_Sensor'")
        print("4. Open Device Manager → Ports (COM & LPT)")
        print("5. Note the COM port number for 'Standard Serial over Bluetooth link'")
        print("6. Update COM_PORT in this script")
        print("\nAfter pairing, restart this script")
        
        input("\nPress Enter to exit...")
        sys.exit(1)