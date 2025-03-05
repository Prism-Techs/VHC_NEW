import tkinter as tk
from tkinter import ttk
from mup4728 import mup4728  # Assuming the provided code is in a file named mup4728.py

class LEDControlApp:
    def __init__(self, root):
        self.root = root
        self.root.title("LED Control Panel")
        
        # Initialize the DAC controller
        self.dac = mup4728(0x61)
        
        # Create a notebook (tabbed interface)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True)
        
        # Create tabs for different LED controls
        self.create_blue_led_tab()
        self.create_green_led_tab()
        self.create_red_led_tab()
        self.create_inner_led_tab()
        self.create_outer_led_tab()
        
    def create_blue_led_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Blue LED")
        
        # Blue LED Voltage Control
        ttk.Label(tab, text="Blue LED Voltage (0-19):").grid(row=0, column=0, padx=10, pady=10)
        self.blue_volt_var = tk.IntVar()
        self.blue_volt_entry = ttk.Entry(tab, textvariable=self.blue_volt_var)
        self.blue_volt_entry.grid(row=0, column=1, padx=10, pady=10)
        
        ttk.Button(tab, text="Set Voltage", command=self.set_blue_voltage).grid(row=0, column=2, padx=10, pady=10)
        
        # Blue LED Frequency Control
        ttk.Label(tab, text="Blue LED Frequency (0-250):").grid(row=1, column=0, padx=10, pady=10)
        self.blue_freq_var = tk.IntVar()
        self.blue_freq_entry = ttk.Entry(tab, textvariable=self.blue_freq_var)
        self.blue_freq_entry.grid(row=1, column=1, padx=10, pady=10)
        
        ttk.Button(tab, text="Set Frequency", command=self.set_blue_frequency).grid(row=1, column=2, padx=10, pady=10)
        
    def create_green_led_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Green LED")
        
        # Green LED Voltage Control
        ttk.Label(tab, text="Green LED Voltage (0-20):").grid(row=0, column=0, padx=10, pady=10)
        self.green_volt_var = tk.IntVar()
        self.green_volt_entry = ttk.Entry(tab, textvariable=self.green_volt_var)
        self.green_volt_entry.grid(row=0, column=1, padx=10, pady=10)
        
        ttk.Button(tab, text="Set Voltage", command=self.set_green_voltage).grid(row=0, column=2, padx=10, pady=10)
        
        # Green LED Frequency Control
        ttk.Label(tab, text="Green LED Frequency (0-15):").grid(row=1, column=0, padx=10, pady=10)
        self.green_freq_var = tk.IntVar()
        self.green_freq_entry = ttk.Entry(tab, textvariable=self.green_freq_var)
        self.green_freq_entry.grid(row=1, column=1, padx=10, pady=10)
        
        ttk.Button(tab, text="Set Frequency", command=self.set_green_frequency).grid(row=1, column=2, padx=10, pady=10)
        
    def create_red_led_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Red LED")
        
        # Red LED Control
        ttk.Label(tab, text="Red LED Voltage (0-20):").grid(row=0, column=0, padx=10, pady=10)
        self.red_volt_var = tk.IntVar()
        self.red_volt_entry = ttk.Entry(tab, textvariable=self.red_volt_var)
        self.red_volt_entry.grid(row=0, column=1, padx=10, pady=10)
        
        ttk.Button(tab, text="Set Voltage", command=self.set_red_voltage).grid(row=0, column=2, padx=10, pady=10)
        
    def create_inner_led_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Inner LED")
        
        # Inner LED Control
        ttk.Label(tab, text="Inner LED Voltage (0-20):").grid(row=0, column=0, padx=10, pady=10)
        self.inner_volt_var = tk.IntVar()
        self.inner_volt_entry = ttk.Entry(tab, textvariable=self.inner_volt_var)
        self.inner_volt_entry.grid(row=0, column=1, padx=10, pady=10)
        
        ttk.Button(tab, text="Set Voltage", command=self.set_inner_voltage).grid(row=0, column=2, padx=10, pady=10)
        
    def create_outer_led_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Outer LED")
        
        # Outer LED Control
        ttk.Label(tab, text="Outer LED Voltage (0-20):").grid(row=0, column=0, padx=10, pady=10)
        self.outer_volt_var = tk.IntVar()
        self.outer_volt_entry = ttk.Entry(tab, textvariable=self.outer_volt_var)
        self.outer_volt_entry.grid(row=0, column=1, padx=10, pady=10)
        
        ttk.Button(tab, text="Set Voltage", command=self.set_outer_voltage).grid(row=0, column=2, padx=10, pady=10)
        
    def set_blue_voltage(self):
        voltage = self.blue_volt_var.get()
        if 0 <= voltage <= 19:
            self.dac.blue_led_volt_control(0, voltage)
        else:
            print("Blue LED Voltage must be between 0 and 19")
        
    def set_blue_frequency(self):
        frequency = self.blue_freq_var.get()
        if 0 <= frequency <= 250:
            self.dac.blue_led_Freq_control(frequency)
        else:
            print("Blue LED Frequency must be between 0 and 250")
        
    def set_green_voltage(self):
        voltage = self.green_volt_var.get()
        if 0 <= voltage <= 20:
            self.dac.green_volt_control(voltage)
        else:
            print("Green LED Voltage must be between 0 and 20")
        
    def set_green_frequency(self):
        frequency = self.green_freq_var.get()
        if 0 <= frequency <= 15:
            self.dac.green_freq_control(frequency)
        else:
            print("Green LED Frequency must be between 0 and 15")
        
    def set_red_voltage(self):
        voltage = self.red_volt_var.get()
        if 0 <= voltage <= 20:
            self.dac.red_led_control(voltage)
        else:
            print("Red LED Voltage must be between 0 and 20")
        
    def set_inner_voltage(self):
        voltage = self.inner_volt_var.get()
        if 0 <= voltage <= 20:
            self.dac.inner_led_control(voltage)
        else:
            print("Inner LED Voltage must be between 0 and 20")
        
    def set_outer_voltage(self):
        voltage = self.outer_volt_var.get()
        if 0 <= voltage <= 20:
            self.dac.outer_led_control(voltage)
        else:
            print("Outer LED Voltage must be between 0 and 20")

if __name__ == "__main__":
    root = tk.Tk()
    app = LEDControlApp(root)
    root.mainloop()