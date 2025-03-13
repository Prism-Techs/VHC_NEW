import tkinter as tk
from tkinter import ttk
import RPi.GPIO as GPIO
from smbus2 import SMBus
import time

# Initialize GPIO and DAC
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# DAC Address and Channels
dac_addr = 0x61
dac_ch = [0, 8, 16, 24, 32, 40, 48, 56]
DAC_lat = 4
GPIO.setup(DAC_lat, GPIO.OUT)
DAC = SMBus(1)

# Reference Voltage (adjust if your DAC uses a different Vref)
VREF = 5.0  # 5V reference voltage for MCP4728 internal reference

# LED Control Functions
def set_dac_value(channel, value):
    """Set DAC value for a specific channel with stability."""
    try:
        GPIO.output(DAC_lat, GPIO.LOW)
        time.sleep(0.01)  # Ensure GPIO settles
        # Add +128 to first byte to match dac_lib_soft.py format
        data = [int(value / 256) + 128, int(value % 256)]
        DAC.write_i2c_block_data(dac_addr, dac_ch[channel], data)
        time.sleep(0.01)  # DAC settling time
        GPIO.output(DAC_lat, GPIO.HIGH)
        time.sleep(0.01)  # Latch stability
        return True
    except Exception as e:
        print(f"DAC write error on channel {channel}: {e}")
        return False

def calculate_voltage(dac_value):
    """Calculate voltage from DAC value (0-4095 -> 0-VREF)."""
    return round((dac_value / 4095) * VREF, 3)

def update_leds():
    """Update all LEDs and display voltages."""
    try:
        # Read and validate input values
        red_value = int(red_entry.get())
        green_value = int(green_entry.get())
        blue_value = int(blue_entry.get())
        inner_value = int(inner_entry.get())
        outer_value = int(outer_entry.get())

        if not all(0 <= val <= 4095 for val in [red_value, green_value, blue_value, inner_value, outer_value]):
            raise ValueError("Values must be between 0 and 4095")

        # Update DAC values
        set_dac_value(6, red_value)    # Red LED (Channel 6)
        set_dac_value(4, green_value)  # Green LED (Channel 4)
        set_dac_value(2, blue_value)   # Blue LED (Channel 2)
        set_dac_value(5, inner_value)  # Inner LED (Channel 5)
        set_dac_value(7, outer_value)  # Outer LED (Channel 7)

        # Calculate voltages
        red_volt = calculate_voltage(red_value)
        green_volt = calculate_voltage(green_value)
        blue_volt = calculate_voltage(blue_value)
        inner_volt = calculate_voltage(inner_value)
        outer_volt = calculate_voltage(outer_value)

        # Update voltage labels
        red_volt_label.config(text=f"{red_volt}V")
        green_volt_label.config(text=f"{green_volt}V")
        blue_volt_label.config(text=f"{blue_volt}V")
        inner_volt_label.config(text=f"{inner_volt}V")
        outer_volt_label.config(text=f"{outer_volt}V")

        # Update status
        status_label.config(text=f"LEDs Updated! Voltages - Red: {red_volt}V, Green: {green_volt}V, "
                           f"Blue: {blue_volt}V, Inner: {inner_volt}V, Outer: {outer_volt}V", fg="green")
    except ValueError as e:
        status_label.config(text=str(e) or "Invalid Input! Enter numbers 0-4095 only.", fg="red")
    except Exception as e:
        status_label.config(text=f"Error updating LEDs: {e}", fg="red")

# Create the GUI
root = tk.Tk()
root.title("Real-Time LED Control with Voltage Display")
root.geometry("500x400")

# Input Boxes and Voltage Labels
ttk.Label(root, text="Red LED Value (0-4095):").grid(row=0, column=0, padx=10, pady=5)
red_entry = ttk.Entry(root)
red_entry.grid(row=0, column=1, padx=10, pady=5)
red_entry.insert(0, "0")
red_volt_label = ttk.Label(root, text="0.000V", font=("Arial", 10))
red_volt_label.grid(row=0, column=2, padx=5)

ttk.Label(root, text="Green LED Value (0-4095):").grid(row=1, column=0, padx=10, pady=5)
green_entry = ttk.Entry(root)
green_entry.grid(row=1, column=1, padx=10, pady=5)
green_entry.insert(0, "0")
green_volt_label = ttk.Label(root, text="0.000V", font=("Arial", 10))
green_volt_label.grid(row=1, column=2, padx=5)

ttk.Label(root, text="Blue LED Value (0-4095):").grid(row=2, column=0, padx=10, pady=5)
blue_entry = ttk.Entry(root)
blue_entry.grid(row=2, column=1, padx=10, pady=5)
blue_entry.insert(0, "0")
blue_volt_label = ttk.Label(root, text="0.000V", font=("Arial", 10))
blue_volt_label.grid(row=2, column=2, padx=5)

ttk.Label(root, text="Inner LED Value (0-4095):").grid(row=3, column=0, padx=10, pady=5)
inner_entry = ttk.Entry(root)
inner_entry.grid(row=3, column=1, padx=10, pady=5)
inner_entry.insert(0, "0")
inner_volt_label = ttk.Label(root, text="0.000V", font=("Arial", 10))
inner_volt_label.grid(row=3, column=2, padx=5)

ttk.Label(root, text="Outer LED Value (0-4095):").grid(row=4, column=0, padx=10, pady=5)
outer_entry = ttk.Entry(root)
outer_entry.grid(row=4, column=1, padx=10, pady=5)
outer_entry.insert(0, "0")
outer_volt_label = ttk.Label(root, text="0.000V", font=("Arial", 10))
outer_volt_label.grid(row=4, column=2, padx=5)

# Update Button
update_button = ttk.Button(root, text="Update LEDs", command=update_leds)
update_button.grid(row=5, column=0, columnspan=3, pady=10)

# Status Label
status_label = ttk.Label(root, text="Enter values and click Update LEDs", font=("Arial", 10))
status_label.grid(row=6, column=0, columnspan=3, pady=5)

# Run the GUI
root.mainloop()

# Cleanup GPIO on exit
GPIO.cleanup()