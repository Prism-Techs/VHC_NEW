import tkinter as tk
from tkinter import ttk
import RPi.GPIO as GPIO
from smbus2 import SMBus

# Initialize GPIO and DAC (same as your original code)
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
DAC = SMBus(1)
dac_addr = 0x61  # Change if your DAC has a different address

# DAC Channels (from your code)
dac_ch = [0, 8, 16, 24, 32, 40, 48, 56]

class GreenLEDControl:
    def __init__(self, root):
        self.root = root
        self.root.title("Green LED Brightness Control")
        
        # Variables
        self.voltage = tk.IntVar(value=20)  # Default to max (20)
        self.frequency = tk.IntVar(value=2000)  # Default frequency (Hz)
        
        # UI Setup
        self.setup_ui()

    def setup_ui(self):
        # Frame
        frame = ttk.Frame(self.root, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Brightness Slider
        ttk.Label(frame, text="Brightness (0-20):").pack()
        self.slider = ttk.Scale(
            frame,
            from_=0,
            to=20,
            variable=self.voltage,
            command=self.update_brightness,
            orient=tk.HORIZONTAL
        )
        self.slider.pack(fill=tk.X)
        
        # Frequency Control
        ttk.Label(frame, text="Frequency (Hz):").pack()
        self.freq_entry = ttk.Entry(frame, textvariable=self.frequency)
        self.freq_entry.pack()
        ttk.Button(frame, text="Set Frequency", command=self.set_frequency).pack()
        
        # Apply Button
        ttk.Button(frame, text="Apply Settings", command=self.apply_settings).pack(pady=10)
        
        # Status Label
        self.status = ttk.Label(frame, text="Ready")
        self.status.pack()

    def update_brightness(self, event=None):
        """Update brightness in real-time while sliding."""
        voltage = self.voltage.get()
        self.status.config(text=f"Brightness: {voltage}/20")

    def set_frequency(self):
        """Set green LED frequency."""
        try:
            freq = int(self.frequency.get())
            dac_val = int(freq / 1.62)  # From your original code
            data = [int(dac_val / 256), int(dac_val % 256)]
            DAC.write_i2c_block_data(dac_addr, dac_ch[3], data)  # GREEN_FREQ channel
            self.status.config(text=f"Frequency set to {freq} Hz")
        except ValueError:
            self.status.config(text="Invalid frequency!")

    def apply_settings(self):
        """Apply voltage and frequency settings."""
        voltage = self.voltage.get()
        freq = self.frequency.get()
        
        # Set voltage (from your green_volt_control method)
        dac_val = int(300 * voltage + 0.380952)  # Adjust multiplier if needed
        data = [int(dac_val / 256), int(dac_val % 256)]
        DAC.write_i2c_block_data(dac_addr, dac_ch[4], data)  # GREEN_Volt channel
        
        # Set frequency
        self.set_frequency()
        
        self.status.config(text=f"Applied: Brightness={voltage}, Freq={freq} Hz")

    def cleanup(self):
        """Cleanup GPIO and DAC on close."""
        GPIO.cleanup()
        DAC.close()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = GreenLEDControl(root)
    root.protocol("WM_DELETE_WINDOW", app.cleanup)
    root.mainloop()