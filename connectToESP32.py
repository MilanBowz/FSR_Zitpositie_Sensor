# serial_ble_client.py
import serial
import serial.tools.list_ports
import time
import sys
import matplotlib
matplotlib.use('TkAgg')  # Set backend before importing pyplot
import matplotlib.pyplot as plt
import threading
import queue
import warnings
import atexit
import os

warnings.filterwarnings("ignore")  # Suppress all warnings

# Check if plotter exists
try:
    from plotter import SimplePlotter
    TOON_GRAFIEK = True
except ImportError:
    print("Plotter not available, running in text-only mode")
    TOON_GRAFIEK = False

# CONFIGURATION
COM_PORT = "COM18"
BAUD_RATE = 9600

class PlotterThread(threading.Thread):
    """Separate thread for handling the plotter"""
    def __init__(self, max_points=400, window_seconds=8):
        super().__init__()
        self.plotter = None
        self.max_points = max_points
        self.window_seconds = window_seconds
        self.data_queue = queue.Queue(maxsize=1000)
        self.running = True
        self.daemon = True
        self.is_alive_flag = True
        
    def run(self):
        """Run the plotter in a separate thread"""
        try:
            # Suppress warnings in this thread
            import warnings
            warnings.filterwarnings("ignore")
            
            self.plotter = SimplePlotter(
                max_points=self.max_points, 
                window_seconds=self.window_seconds
            )
            
            while self.running and self.plotter and not self.plotter.is_window_closed():
                try:
                    data = self.data_queue.get(timeout=0.05)
                    if data is None:
                        break
                    
                    avg, volt = data
                    if self.plotter:
                        self.plotter.voeg_toe(avg, volt)
                        
                except queue.Empty:
                    if self.plotter:
                        try:
                            # Very short pause
                            plt.pause(0.001)
                        except:
                            pass
                    continue
                    
        except Exception:
            pass  # Silently ignore thread errors
        finally:
            self.is_alive_flag = False
            # Don't try to close plotter here - let main thread handle it
    
    def add_data(self, avg, volt):
        """Add data to the queue"""
        if self.running and self.plotter and not self.plotter.is_window_closed():
            try:
                self.data_queue.put_nowait((avg, volt))
                return True
            except:
                pass
        return False
    
    def is_window_closed(self):
        """Check if window is closed"""
        if self.plotter:
            return self.plotter.is_window_closed()
        return False
    
    def stop(self):
        """Stop the plotter thread"""
        self.running = False
        # Don't close plotter here - let main thread handle it

def find_esp32_com_port():
    """Automatically find ESP32 Bluetooth COM port"""
    ports = serial.tools.list_ports.comports()
    for port in ports:
        if "Bluetooth" in port.description or "Standard Serial" in port.description:
            return port.device
    return None

def cleanup_plotter(plotter_thread):
    """Clean up plotter safely"""
    if plotter_thread:
        try:
            plotter_thread.running = False
            if plotter_thread.plotter:
                # Force close without waiting for thread
                try:
                    plt.close('all')
                except:
                    pass
        except:
            pass

def connect_and_read():
    """Connect to ESP32 and read data"""
    
    port_to_use = COM_PORT
    if port_to_use == "COM3":
        auto_port = find_esp32_com_port()
        if auto_port:
            port_to_use = auto_port
            print(f"Auto-detected COM port: {port_to_use}")
    
    print(f"\n{'='*50}")
    print(f"ESP32 Bluetooth SPP Client")
    print(f"COM Port: {port_to_use}")
    print(f"Baud Rate: {BAUD_RATE}")
    print(f"{'='*50}\n")
    
    plotter_thread = None
    if TOON_GRAFIEK:
        try:
            plotter_thread = PlotterThread(max_points=500, window_seconds=8)
            plotter_thread.start()
            time.sleep(0.5)
        except Exception as e:
            print(f"⚠ Grafiek niet beschikbaar: {e}\n")
            plotter_thread = None
    
    # Register cleanup
    def cleanup():
        cleanup_plotter(plotter_thread)
    atexit.register(cleanup)
    
    ser = None
    try:
        print(f"Connecting to {port_to_use}...")
        ser = serial.Serial(
            port=port_to_use,
            baudrate=BAUD_RATE,
            timeout=0.05,
            write_timeout=1
        )
        
        print(f"✓ Connected to ESP32!\n")
        print("Waiting for data... (Press Ctrl+C or close graph to stop)\n")
        print("-" * 50)
        
        packet_count = 0
        last_status_time = time.time()
        
        time.sleep(1)
        ser.reset_input_buffer()
        
        while True:
            if plotter_thread and plotter_thread.is_window_closed():
                break
            
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8', errors='ignore').strip()
                
                if line and "AVG:" in line and "RAW:" in line:
                    try:
                        parts = line.split(',')
                        avg = float(parts[0].split(':')[1].strip())
                        raw = float(parts[1].split(':')[1].strip())
                        packet_count += 1
                        
                        if packet_count % 100 == 0:
                            print(f"[{packet_count:5d}] AVG: {avg:.1f}, RAW: {raw:.2f}")
                        
                        if plotter_thread:
                            if not plotter_thread.add_data(avg, raw):
                                if plotter_thread.is_window_closed():
                                    break
                                
                    except:
                        pass
            
            if time.time() - last_status_time >= 3 and packet_count > 0:
                rate = packet_count / (time.time() - last_status_time + 0.01)
                queue_size = plotter_thread.data_queue.qsize() if plotter_thread else 0
                print(f"\n[STATUS] Packets: {packet_count} | Rate: {rate:.1f} Hz | Queue: {queue_size}")
                print("-" * 50)
                last_status_time = time.time()
            
            time.sleep(0.001)
            
    except serial.SerialException as e:
        print(f"\n❌ ERROR: Could not open {port_to_use}: {e}")
        return False
    except KeyboardInterrupt:
        print("\n\n✓ Stopped by user")
    finally:
        # Clean up in correct order
        if plotter_thread:
            print("\nClosing graph...")
            plotter_thread.running = False
            time.sleep(0.1)
            
            # Close all plots safely
            try:
                plt.close('all')
            except:
                pass
            
            # Clear any remaining matplotlib figures
            try:
                import matplotlib._pylab_helpers
                for manager in matplotlib._pylab_helpers.Gcf.get_all_fig_managers():
                    try:
                        plt.close(manager.num)
                    except:
                        pass
            except:
                pass
        
        if ser and ser.is_open:
            ser.close()
            print("Serial connection closed")
    
    return True

def main():
    """Main function"""
    print("ESP32 Bluetooth SPP Client for Windows 11")
    print("=" * 50)
    
    print("\nAvailable COM ports:")
    for port in serial.tools.list_ports.comports():
        print(f"  {port.device}: {port.description}")
    
    print("\n" + "=" * 50)
    
    success = connect_and_read()
    
    if not success:
        print("\nTroubleshooting Guide:")
        print("=====================")
        print("1. Pair ESP32 with Windows in Bluetooth settings")
        print("2. Check COM port in Device Manager")
        print("3. Update COM_PORT in script if needed")
        input("\nPress Enter to exit...")
        sys.exit(1)
    
    print("\n App closed successfully")
    # Force exit without waiting for thread cleanup
    os._exit(0)

if __name__ == "__main__":
    main()