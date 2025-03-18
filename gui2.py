import tkinter as tk
from tkinter import ttk
import RPi.GPIO as GPIO
from smbus2 import SMBus
import time
import math

# GPIO Pin Details
print_en = 0
DAC_lat = 4
B_F_I = 27
B_E = 12
G_F_I = 13
G_E = 26
SW_I = 20
switch = 20
BZ_I = 19
FN_E = 21
Disp = 22
flik_pin = 18

# Fixed Data
b_volt_val = [159, 170, 183, 199, 219, 243, 274, 312, 358, 417, 493, 591, 720, 889, 1111, 1413, 1817, 2376, 3161, 3918]
Actuator_val = [0, 142, 1100, 3680]
b_freq_val = [0, 0, 11, 12, 12, 12, 12, 13, 13, 13, 14, 14, 14, 15, 15, 15, 16, 16, 17, 17, 17, 18, 18, 19, 19, 20, 20, 21, 21, 21, 22, 23, 23, 24, 24, 25, 25, 26, 27, 27, 28, 28, 29, 30, 31, 31, 32, 33, 34, 34, 35, 36, 37, 38, 39, 40, 40, 41, 42, 43, 44, 45, 47, 48, 49, 50, 51, 52, 54, 55, 56, 57, 59, 60, 62, 63, 64, 66, 67, 69, 71, 72, 74, 76, 78, 79, 81, 83, 85, 87, 89, 91, 93, 96, 98, 100, 102, 105, 107, 110, 112, 115, 118, 120, 123, 126, 129, 132, 135, 138, 142, 145, 148, 152, 155, 159, 163, 166, 170, 174, 178, 183, 187, 191, 196, 200, 205, 210, 215, 220, 225, 230, 235, 241, 246, 252, 258, 264, 270, 277, 283, 290, 296, 303, 310, 318, 325, 333, 340, 348, 356, 365, 373, 382, 391, 400, 409, 419, 429, 439, 449, 459, 470, 481, 492, 504, 516, 528, 540, 552, 565, 579, 592, 606, 620, 634, 649, 664, 680, 696, 712, 729, 746, 763, 781, 799, 818, 837, 856, 876, 896, 917, 939, 961, 983, 1006, 1029, 1053, 1078, 1103, 1129, 1155, 1182, 1210, 1238, 1267, 1296, 1326, 1357, 1389, 1421, 1454, 1488, 1523, 1558, 1595, 1632, 1670, 1709, 1749, 1790, 1831, 1874, 1918, 1962, 2008, 2055, 2103, 2152, 2202, 2253, 2306, 2359, 2414, 2471, 2528, 2587, 2647, 2709, 2772, 2837, 2903, 2971, 3040, 3111, 3183, 3257, 3333, 3411, 3490, 3572]

flicker_delay = 0.043
cff_delay = 0.209
brk_delay = 0.125

# DAC Control Class
class mup4728:
    def __init__(self, dac_addr):
        self.DAC = SMBus(1)
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(DAC_lat, GPIO.OUT)
        GPIO.setup(B_E, GPIO.OUT)
        GPIO.setup(G_E, GPIO.OUT)
        GPIO.setup(FN_E, GPIO.OUT)
        GPIO.setup(Disp, GPIO.OUT)
        GPIO.setup(BZ_I, GPIO.OUT)
        GPIO.setup(flik_pin, GPIO.OUT)
        GPIO.output(DAC_lat, GPIO.HIGH)
        GPIO.output(B_E, GPIO.LOW)
        GPIO.output(G_E, GPIO.LOW)
        GPIO.output(FN_E, GPIO.HIGH)
        self.dac_addr = dac_addr
        self.dac_ch = [0, 8, 16, 24, 32, 40, 48, 56]
        self.pwm_run = 0
        # Comment out PWM initialization to disable it completely for now
        # self.p = GPIO.PWM(flik_pin, 35)  # Disabled to isolate interference
        self.last_dac_values = {2: None, 4: None, 6: None, 5: None, 7: None}  # Track all LED DAC values

    def set_dac_value(self, channel, value):
        value = max(0, min(4095, int(value)))
        # Only update if value has changed
        if self.last_dac_values[channel] != value:
            GPIO.output(DAC_lat, GPIO.LOW)
            data = [int(value / 256), int(value % 256)]
            print(f"Set DAC Channel {channel}: Value={value}, Data={data}")
            self.DAC.write_i2c_block_data(self.dac_addr, self.dac_ch[channel], data)
            GPIO.output(DAC_lat, GPIO.HIGH)
            self.last_dac_values[channel] = value
        else:
            print(f"DAC Channel {channel}: No change, Value remains {value}")
        time.sleep(0.01)  # Reduced to 10ms for minimal delay

    def blue_led_volt_control(self, mode, val):
        if mode == 0 and 0 <= val <= 19:
            b_volt = int(b_volt_val[val] * 1.95)
            self.set_dac_value(2, b_volt)
            return b_volt, b_volt * 3.3 / 4095
        elif mode == 1 and 1 <= val <= 20:
            b_volt = int((7.79398 * val - 4.93684) / 1.25)
            self.set_dac_value(2, b_volt)
            return b_volt, b_volt * 3.3 / 4095
        elif mode == 2 and 1 <= val <= 20:
            b_volt = int((24.606 * val - 23.4632) / 1.25)
            self.set_dac_value(2, b_volt)
            return b_volt, b_volt * 3.3 / 4095
        elif mode == 3 and 0 <= val <= 20:
            b_volt = int((28.8 * val + 0.4) / 1)
            self.set_dac_value(2, b_volt)
            return b_volt, b_volt * 3.3 / 4095
        return 0, 0

    def green_volt_control(self, data_in):
        if 0 <= data_in <= 20:
            dac_val = int(85.4 * data_in + 0.380952)
            self.set_dac_value(4, dac_val)
            return dac_val, dac_val * 3.3 / 4095
        return 0, 0

    def red_led_control(self, data_in):
        if 0 <= data_in <= 20:
            dac_val = int(4.80519 * data_in - 0.4329)
            self.set_dac_value(6, dac_val)
            return dac_val, dac_val * 3.3 / 4095
        return 0, 0

    def inner_led_control(self, data_in):
        if 0 <= data_in <= 20:
            dac_val = int(84.4 * data_in)
            dac_val = max(0, min(4095, dac_val))
            str_data = 'INNER_LED_DAC = ' + str(dac_val)
            print(str_data)
            self.set_dac_value(5, dac_val)
            voltage = dac_val * 3.3 / 4095
            print(f"Inner LED: data_in={data_in}, DAC={dac_val}, Voltage={voltage:.2f}V")
            return dac_val, voltage
        else:
            str_data = 'INNER_LED_DAC must be 0 to 20, got ' + str(data_in)
            print(str_data)
            self.set_dac_value(5, 0)
            return 0, 0

    def outer_led_control(self, data_in):
        if 0 <= data_in <= 20:
            dac_val = int(59.4 * data_in - 0.38095)
            self.set_dac_value(7, dac_val)
            return dac_val, dac_val * 3.3 / 4095
        return 0, 0

    def fliker_start_g(self):
        GPIO.output(G_E, GPIO.HIGH)
        GPIO.output(B_E, GPIO.LOW)
        if not self.pwm_run and hasattr(self, 'p'):
            self.p.start(50.0)
            self.pwm_run = 1

    def fliker_start_b(self):
        GPIO.output(G_E, GPIO.HIGH)
        GPIO.output(B_E, GPIO.HIGH)
        if not self.pwm_run and hasattr(self, 'p'):
            self.p.start(50.0)
            self.pwm_run = 1

    def fliker_Freq(self, frq):
        if hasattr(self, 'p'):
            self.p.ChangeFrequency(frq)

    def all_led_off(self):
        self.set_dac_value(2, 0)
        self.set_dac_value(4, 0)
        self.set_dac_value(6, 0)
        self.set_dac_value(5, 0)
        self.set_dac_value(7, 0)
        GPIO.output(G_E, GPIO.LOW)
        GPIO.output(B_E, GPIO.LOW)
        if self.pwm_run and hasattr(self, 'p'):
            self.p.stop()
            self.pwm_run = 0

# Tkinter GUI with Entry Boxes
class LEDControlApp:
    def __init__(self, root):
        self.root = root
        self.root.title("LED Control")
        self.dac = mup4728(0x61)

        self.blue_entry = self.create_entry("Blue LED (0-20)", "0", row=0)
        self.green_entry = self.create_entry("Green LED (0-20)", "0", row=1)
        self.red_entry = self.create_entry("Red LED (0-20)", "0", row=2)
        self.inner_entry = self.create_entry("Inner LED (0-20)", "0", row=3)
        self.outer_entry = self.create_entry("Outer LED (0-20)", "0", row=4)

        self.blue_label = self.create_label("Blue: DAC=0, Voltage=0.00V", row=0, column=3)
        self.green_label = self.create_label("Green: DAC=0, Voltage=0.00V", row=1, column=3)
        self.red_label = self.create_label("Red: DAC=0, Voltage=0.00V", row=2, column=3)
        self.inner_label = self.create_label("Inner: DAC=0, Voltage=0.00V", row=3, column=3)
        self.outer_label = self.create_label("Outer: DAC=0, Voltage=0.00V", row=4, column=3)

        self.flicker_freq_entry = self.create_entry("Flicker Frequency (1-100 Hz)", "35", row=5)
        self.flicker_start_g_button = ttk.Button(root, text="Start Green Flicker", command=self.start_green_flicker)
        self.flicker_start_g_button.grid(row=6, column=0, padx=10, pady=10)
        self.flicker_start_b_button = ttk.Button(root, text="Start Blue Flicker", command=self.start_blue_flicker)
        self.flicker_start_b_button.grid(row=6, column=1, padx=10, pady=10)
        self.flicker_stop_button = ttk.Button(root, text="Stop Flicker", command=self.stop_flicker)
        self.flicker_stop_button.grid(row=6, column=2, padx=10, pady=10)

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
            blue_val = int(self.blue_entry.get())
            green_val = int(self.green_entry.get())
            red_val = int(self.red_entry.get())
            inner_val = int(self.inner_entry.get())
            outer_val = int(self.outer_entry.get())

            blue_val = max(0, min(20, blue_val))
            green_val = max(0, min(20, green_val))
            red_val = max(0, min(20, red_val))
            inner_val = max(0, min(20, inner_val))
            outer_val = max(0, min(20, outer_val))

            blue_dac, blue_voltage = self.dac.blue_led_volt_control(0, blue_val)
            green_dac, green_voltage = self.dac.green_volt_control(green_val)
            red_dac, red_voltage = self.dac.red_led_control(red_val)
            inner_dac, inner_voltage = self.dac.inner_led_control(inner_val)
            outer_dac, outer_voltage = self.dac.outer_led_control(outer_val)

            self.blue_label.config(text=f"Blue: DAC={blue_dac}, Voltage={blue_voltage:.2f}V")
            self.green_label.config(text=f"Green: DAC={green_dac}, Voltage={green_voltage:.2f}V")
            self.red_label.config(text=f"Red: DAC={red_dac}, Voltage={red_voltage:.2f}V")
            self.inner_label.config(text=f"Inner: DAC={inner_dac}, Voltage={inner_voltage:.2f}V")
            self.outer_label.config(text=f"Outer: DAC={outer_dac}, Voltage={outer_voltage:.2f}V")
            
        except ValueError:
            print("Please enter valid numeric values")

    def start_green_flicker(self):
        try:
            freq = int(self.flicker_freq_entry.get())
            freq = max(1, min(100, freq))
            self.dac.fliker_start_g()
            self.dac.fliker_Freq(freq)
        except ValueError:
            print("Please enter a valid numeric frequency")

    def start_blue_flicker(self):
        try:
            freq = int(self.flicker_freq_entry.get())
            freq = max(1, min(100, freq))
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