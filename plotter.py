# plotter.py - Oscilloscope-style scrolling display (Single graph - optimized)
import matplotlib
matplotlib.use('TkAgg')  # Explicitly set backend
import matplotlib.pyplot as plt
from collections import deque
import time
import sys
import warnings
warnings.filterwarnings("ignore", category=UserWarning)  # Suppress thread warnings

class SimplePlotter:
    def __init__(self, max_points=400, window_seconds=10):
        self.max_points = max_points
        self.window_seconds = window_seconds
        self.tijden = deque(maxlen=max_points)
        self.avg_waarden = deque(maxlen=max_points)
        self.start_tijd = time.time()
        self.is_closed = False
        self.paused = False
        
        # Create figure in main thread
        self.fig, self.ax = plt.subplots(1, 1, figsize=(12, 6))
        
        # Setup plot
        self.line, = self.ax.plot([], [], 'b-', linewidth=1.5)
        
        # Styling
        self.ax.set_ylabel('Average Value', fontsize=12)
        self.ax.set_xlabel('Tijd (seconden)', fontsize=12)
        self.ax.set_title('ESP32 Sensor Data - Live (Oscilloscope Mode)', fontsize=14)
        self.ax.grid(True, alpha=0.3)
        self.ax.set_facecolor('#f8f9fa')
        
        # Set fixed window width
        self.ax.set_xlim(0, window_seconds)
        self.ax.set_ylim(0, 100)
        
        # Trigger indicator
        self.trigger_line = self.ax.axvline(x=0, color='g', linestyle='--', alpha=0.5, linewidth=1)
        
        plt.tight_layout()
        plt.ion()
        plt.show(block=False)
        
        # Connect events
        self.fig.canvas.mpl_connect('close_event', self.on_close)
        self.fig.canvas.mpl_connect('key_press_event', self.on_key_press)
        
        self.update_count = 0
        self.last_trigger_time = 0
        
        print("  📊 Oscilloscope mode - Fixed time window (%.1f seconds)" % window_seconds)
        print("  ⚡ Single graph mode for maximum performance")
        print("  ⌨️  Press 'p' to pause/resume, 'r' to reset view, 't' to show trigger")
    
    def on_close(self, event):
        """Handle window close event"""
        self.is_closed = True
        
    def on_key_press(self, event):
        """Handle keyboard shortcuts"""
        if event.key == 'p':
            self.paused = not self.paused
            print(f"\n{'⏸ Paused' if self.paused else '▶ Resumed'}")
        elif event.key == 'r':
            self.reset_view()
            print("\n🔄 View reset")
        elif event.key == 't':
            self.show_trigger()
    
    def is_window_closed(self):
        """Check if window has been closed"""
        if self.is_closed:
            return True
        try:
            if not plt.fignum_exists(self.fig.number):
                self.is_closed = True
                return True
        except:
            pass
        return False
    
    def reset_view(self):
        """Reset y-axis limits to auto-scale"""
        if self.avg_waarden:
            avg_min = min(self.avg_waarden)
            avg_max = max(self.avg_waarden)
            margin = max(5, (avg_max - avg_min) * 0.2)
            self.ax.set_ylim(max(0, avg_min - margin), avg_max + margin)
        self.ax.set_xlim(0, self.window_seconds)
    
    def show_trigger(self):
        """Show trigger indicator at current time"""
        if self.tijden:
            current_time = self.tijden[-1]
            self.trigger_line.set_xdata([current_time, current_time])
            self.last_trigger_time = current_time
            print(f"Trigger at t = {current_time:.2f}s")
    
    def voeg_toe(self, avg, volt=None):
        """Add data point and update plot"""
        if self.is_window_closed() or self.paused:
            return not self.is_window_closed()
        
        huidige_tijd = time.time() - self.start_tijd
        self.tijden.append(huidige_tijd)
        self.avg_waarden.append(avg)
        
        self.update_count += 1
        if self.update_count % 2 == 0:
            self._update_plot()
        
        return True
    
    def _update_plot(self):
        """Update the plot with oscilloscope-style scrolling"""
        if len(self.tijden) < 2:
            return
        
        try:
            tijden_list = list(self.tijden)
            avg_list = list(self.avg_waarden)
            
            self.line.set_data(tijden_list, avg_list)
            
            if tijden_list:
                current_time = tijden_list[-1]
                
                if current_time > self.window_seconds:
                    x_min = max(0, current_time - self.window_seconds)
                    x_max = current_time
                    x_padding = self.window_seconds * 0.05
                    self.ax.set_xlim(x_min - x_padding, x_max + x_padding)
                    
                    if hasattr(self, 'trigger_line') and self.last_trigger_time > 0:
                        visible = (self.last_trigger_time >= x_min and 
                                  self.last_trigger_time <= x_max)
                        self.trigger_line.set_visible(visible)
                else:
                    self.ax.set_xlim(0, self.window_seconds)
                
                if avg_list:
                    visible_avg = [v for v in avg_list if v is not None]
                    if visible_avg:
                        avg_min = min(visible_avg)
                        avg_max = max(visible_avg)
                        margin = max(5, (avg_max - avg_min) * 0.15)
                        self.ax.set_ylim(max(0, avg_min - margin), avg_max + margin)
            
            if self.avg_waarden and len(tijden_list) > 1:
                time_diff = tijden_list[-1] - tijden_list[-2]
                freq_info = f" | {1.0/time_diff:.1f} Hz" if time_diff > 0 else ""
                self.ax.set_title(
                    f'ESP32 Sensor Data - Live | AVG: {self.avg_waarden[-1]:.1f}{freq_info}',
                    fontsize=14, fontweight='bold'
                )
            
            self.fig.canvas.draw_idle()
            self.fig.canvas.flush_events()
        except:
            self.is_closed = True
    
    def sluit(self):
        """Close the plot safely"""
        try:
            self.is_closed = True
            if hasattr(self, 'fig') and self.fig:
                plt.close(self.fig)
        except:
            pass