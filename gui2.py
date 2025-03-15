import tkinter as tk
from tkinter import ttk
import RPi.GPIO as GPIO
from smbus2 import SMBus
import time
import math

# GPIO Pin Details and Fixed Data remain unchanged
# ... [Previous GPIO and fixed data definitions remain the same] ...

# DAC Control Class remains unchanged
class mup4728:
    # ... [Previous mup4728 class definition remains the same] ...

# Modified Tkinter GUI with Entry widgets instead of sliders
class LEDControlApp:
    def __init__(self, root):
        self.root = root
        self.root.title("LED Control")
        self.dac = mup4728(0x61)

        # Entry boxes for LED control
        self.blue_entry = self.create_entry("Blue LED (0-20)", "0", row=0)
        self.green_entry = self.create_entry("Green LED (0-20)", "0", row=1)
        self.red_entry = self.create_entry("Red LED (0-20)", "0", row=2)
        self.inner_entry = self.create_entry("Inner LED (0-20)", "0", row=3)
        self.outer_entry = self.create_entry("Outer LED (0-20)", "0", row=4)

        # Labels for displaying DAC values and voltages
        self.blue_label = self.create_label("Blue: DAC=0, Voltage=0.00V", row=0, column=3)
        self.green_label = self.create_label("Green: DAC=0, Voltage=0.00V", row=1, column=3)
        self.red_label = self.create_label("Red: DAC=0, Voltage=0.00V", row=2, column=3)
        self.inner_label = self.create_label("Inner: DAC=0, Voltage=0.00V", row=3, column=3)
        self.outer_label = self.create_label("Outer: DAC=0, Voltage=0.00V", row=4, column=3)

        # Flicker control with entry box
        self.flicker_freq_entry = self.create_entry("Flicker Frequency (1-100 Hz)", "35", row=5)
        self.flicker_start_g_button = ttk.Button(root, text="Start Green Flicker", command=self.start_green_flicker)
        self.flicker_start_g_button.grid(row=6, column=0, padx=10, pady=10)
        self.flicker_start_b_button = ttk.Button(root, text="Start Blue Flicker", command=self.start_blue_flicker)
        self.flicker_start_b_button.grid(row=6, column=1, padx=10, pady=10)
        self.flicker_stop_button = ttk.Button(root, text="Stop Flicker", command=self.stop_flicker)
        self.flicker_stop_button.grid(row=6, column=2, padx=10, pady=10)

        # Update button
        self.update_button = ttk.Button(root, text="Update LEDs", command=self.update_leds)
        self.update_button.grid(row=7, column=0, columnspan=3, padx=10, pady=10)

    def create_entry(self, label, default, row):
        ttk.Label(self.root, text=label).grid(row=row, column=0, padx=10, pady=5)
        entry = ttk.Entry(self.root, width=10)
        entry.insert(0, default)
        entry.grid(row=row, column=1, padx=10, pady=5)
        return entry

    def create_label(self, text, row, column):
        label = ttk.Label(self.root, text=text)
        label.grid(row=row, column=column, padx=10, pady=5)
        return label

    def update_leds(self):
        try:
            # Get values from entry boxes and validate
            blue_val = int(self.blue_entry.get())
            green_val = int(self.green_entry.get())
            red_val = int(self.red_entry.get())
            inner_val = int(self.inner_entry.get())
            outer_val = int(self.outer_entry.get())

            # Ensure values are within valid range (0-20)
            blue_val = max(0, min(20, blue_val))
            green_val = max(0, min(20, green_val))
            red_val = max(0, min(20, red_val))
            inner_val = max(0, min(20, inner_val))
            outer_val = max(0, min(20, outer_val))

            # Update LED values
            blue_dac, blue_voltage = self.dac.blue_led_volt_control(0, blue_val)
            green_dac, green_voltage = self.dac.green_volt_control(green_val)
            red_dac, red_voltage = self.dac.red_led_control(red_val)
            inner_dac, inner_voltage = self.dac.inner_led_control(inner_val)
            outer_dac, outer_voltage = self.dac.outer_led_control(outer_val)

            # Update labels with DAC values and voltages
            self.blue_label.config(text=f"Blue: DAC={blue_dac}, Voltage={blue_voltage:.2f}V")
            self.green_label.config(text=f"Green: DAC={green_dac}, Voltage={green_voltage:.2f}V")
            self.red_label.config(text=f"Red: DAC={red_dac}, Voltage={red_voltage:.2f}V")
            self.inner_label.config(text=f"Inner: DAC={inner_dac}, Voltage={inner_voltage:.2f}V")
            self.outer_label.config(text=f"Outer: DAC={outer_dac}, Voltage={outer_voltage:.2f}V")
            
        except ValueError:
            # Handle invalid input (non-numeric values)
            print("Please enter valid numeric values")

    def start_green_flicker(self):
        try:
            freq = int(self.flicker_freq_entry.get())
            freq = max(1, min(100, freq))  # Ensure frequency is between 1-100 Hz
            self.dac.fliker_start_g()
            self.dac.fliker_Freq(freq)
        except ValueError:
            print("Please enter a valid numeric frequency")

    def start_blue_flicker(self):
        try:
            freq = int(self.flicker_freq_entry.get())
            freq = max(1, min(100, freq))  # Ensure frequency is between 1-100 Hz
            self.dac.fliker_start_b()
            self.dac.fliker_Freq(freq)
        except ValueError:
            print("Please enter a valid numeric frequency")

    def stop_flicker(self):
        self.dac.all_led_off()

# Main application
if __name__ == "__main__":
    root = tk.Tk()
    app = LEDControlApp(root)
    root.mainloop()
    GPIO.cleanup()