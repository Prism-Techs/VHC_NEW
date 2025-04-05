import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import time
import re
from header import HeaderComponent
from PIL import Image, ImageTk
import os

class WifiConnectionWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Vekaria Healthcare - WiFi Connection")
        self.root.configure(bg="#1F2937")
        
        # Colors for dark theme
        self.bg_color = "#1F2937"
        self.text_color = "#FFFFFF"
        self.button_bg = "#000000"
        self.button_fg = "#FFFFFF"
        self.button_active_bg = "#333333"
        self.entry_bg = "#2C3E50"
        self.border_color = "#4B5563"
        self.list_bg = "#2C3E50"
        
        # Fonts
        self.title_font = ("Arial", 16, "bold")
        self.normal_font = ("Arial", 12)
        self.button_font = ("Arial", 12)
        
        self.create_header()
        self.create_content()
        
        # Store previously detected networks to check for new ones
        self.previous_networks = set()
        self.wifi_networks = []
        
        # Start periodic scanning
        self.scan_networks_periodically()
    
    def create_header(self):
        """Create the header with logo, company name, version, and title"""
        self.header_frame = tk.Frame(self.root, bg='#1f2836', height=41)
        self.header_frame.pack(fill='x')
        
        # Keep reference of the image to prevent garbage collection
        self.images = {}
        
        # Get current directory and construct absolute paths
        current_dir = os.path.dirname(os.path.realpath(__file__))
        logo_path = os.path.join(current_dir, "logo.png")
        
        # Setup company logo
        try:
            logo = Image.open(logo_path)
            logo = logo.resize((44, 23))
            self.images['logo'] = ImageTk.PhotoImage(logo)
            self.logo_label = tk.Label(
                self.header_frame, 
                image=self.images['logo'],
                bg='#1f2836'
            )
            self.logo_label.place(x=10, y=9)  # Adjusted for left alignment
        except Exception as e:
            print(f"Logo image not found: {e}")
            print(f"Attempted path: {logo_path}")
        
        # Company name label
        tk.Label(
            self.header_frame,
            text="Vekaria Healthcare",
            font=('Helvetica Neue', 14, 'bold'),  # Slightly smaller font for fit
            bg='#1f2836',
            fg='white'
        ).place(x=60, y=10)
        
        # Version label (aligned to the right within 500px width)
        tk.Label(
            self.header_frame,
            text="V1.0",
            font=('Helvetica Neue', 12, 'bold'),  # Slightly smaller font
            bg='#1f2836',
            fg='white'
        ).place(x=450, y=12)  # Adjusted to fit within 500px width
        
        # Page title (below header, full width)
        self.title_label = tk.Label(
            self.root,
            text="WiFi Page",
            font=("Arial", 18),  # Slightly smaller font for better fit
            bg='#1f2836',  # Match header background
            fg='white'
        )
        self.title_label.place(x=10, y=41)  # Positioned just below header
    
    def create_content(self):
        """Create the main content area"""
        self.content_frame = tk.Frame(self.root, bg=self.bg_color)
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(70, 20))  # Adjusted pady to fit header
        
        self.network_frame = tk.Frame(self.content_frame, bg=self.bg_color)
        self.network_frame.pack(fill=tk.X, pady=10)
        
        self.network_label = tk.Label(self.network_frame, text="Available Networks", 
                                     font=self.normal_font, bg=self.bg_color, fg=self.text_color)
        self.network_label.pack(anchor="w")
        
        self.list_frame = tk.Frame(self.content_frame, bg=self.bg_color)
        self.list_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.scrollbar = tk.Scrollbar(self.list_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.network_listbox = tk.Listbox(self.list_frame, 
                                        bg=self.list_bg, 
                                        fg=self.text_color,
                                        selectbackground="#4B5563",
                                        selectforeground="white",
                                        font=self.normal_font,
                                        height=8,  # Increased height for better visibility
                                        bd=1,
                                        highlightthickness=1,
                                        highlightbackground=self.border_color)
        self.network_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.scrollbar.config(command=self.network_listbox.yview)
        self.network_listbox.config(yscrollcommand=self.scrollbar.set)
        
        self.network_listbox.bind("<<ListboxSelect>>", self.on_network_select)
        
        self.scan_button_frame = tk.Frame(self.content_frame, bg=self.bg_color)
        self.scan_button_frame.pack(fill=tk.X, pady=10)
        
        self.scan_button = self.create_button(self.scan_button_frame, "Scan Networks", self.scan_networks)
        self.scan_button.pack(side=tk.LEFT, padx=5)
        
        self.rescan_button = self.create_button(self.scan_button_frame, "Refresh", self.scan_networks)
        self.rescan_button.pack(side=tk.LEFT, padx=5)
        
        self.password_frame = tk.Frame(self.content_frame, bg=self.bg_color)
        self.password_frame.pack(fill=tk.X, pady=10)
        
        self.password_label = tk.Label(self.password_frame, text="Password:", 
                                      font=self.normal_font, bg=self.bg_color, fg=self.text_color)
        self.password_label.pack(side=tk.LEFT, padx=(0, 10))
        
        self.password_entry = tk.Entry(self.password_frame, 
                                      bg=self.entry_bg, 
                                      fg=self.text_color,
                                      font=self.normal_font,
                                      show="*",
                                      bd=1,
                                      highlightthickness=1,
                                      highlightbackground=self.border_color)
        self.password_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.show_password = False
        self.show_password_button = self.create_button(self.password_frame, "Show", self.toggle_password_visibility)
        self.show_password_button.pack(side=tk.RIGHT, padx=5)
        
        self.options_frame = tk.Frame(self.content_frame, bg=self.bg_color)
        self.options_frame.pack(fill=tk.X, pady=10)
        
        self.connect_button = self.create_button(self.options_frame, "Connect", self.connect_wifi)
        self.connect_button.pack(side=tk.LEFT, padx=5)
        
        self.disconnect_button = self.create_button(self.options_frame, "Disconnect", self.disconnect_wifi)
        self.disconnect_button.pack(side=tk.LEFT, padx=5)
        
        self.forget_button = self.create_button(self.options_frame, "Forget Network", self.forget_network)
        self.forget_button.pack(side=tk.LEFT, padx=5)
        
        self.status_label = tk.Label(self.content_frame, 
                                    text="Not connected", 
                                    font=self.normal_font, 
                                    bg=self.bg_color, 
                                    fg="#FF6B6B")
        self.status_label.pack(pady=10)
        
        self.disconnect_button.config(state=tk.DISABLED)
        self.forget_button.config(state=tk.DISABLED)
    
    def create_button(self, parent, text, command):
        """Helper function to create styled buttons"""
        return tk.Button(parent,
                        text=text,
                        font=self.button_font,
                        command=command,
                        bg=self.button_bg,
                        fg=self.button_fg,
                        activebackground=self.button_active_bg,
                        activeforeground=self.button_fg,
                        relief=tk.FLAT,
                        bd=1,
                        highlightbackground=self.border_color,
                        padx=10,
                        pady=5)
    
    def scan_wifi_networks(self):
        """Scan for available WiFi networks using iwlist"""
        try:
            result = subprocess.run(['sudo', 'iwlist', 'wlan0', 'scan'], 
                                  capture_output=True, text=True, check=True)
            output = result.stdout
            
            networks = []
            ssid = None
            signal = None
            secured = False
            
            for line in output.splitlines():
                line = line.strip()
                if "ESSID:" in line:
                    match = re.search(r'ESSID:"(.+)"', line)
                    if match:
                        ssid = match.group(1)
                elif "Signal level" in line:
                    match = re.search(r'Signal level=(-?\d+)', line)
                    if match:
                        signal = int(match.group(1))
                elif "Encryption key:on" in line:
                    secured = True
                elif "Cell" in line and ssid:
                    if ssid and signal is not None:
                        signal_str = "Strong" if signal > -50 else "Medium" if signal > -70 else "Weak"
                        networks.append({"name": ssid, "signal": signal_str, "secured": secured})
                    ssid = None
                    signal = None
                    secured = False
            
            if ssid and signal is not None:
                signal_str = "Strong" if signal > -50 else "Medium" if signal > -70 else "Weak"
                networks.append({"name": ssid, "signal": signal_str, "secured": secured})
            
            return networks
        except subprocess.CalledProcessError as e:
            print(f"Error scanning networks: {e}")
            return []
        except Exception as e:
            print(f"Unexpected error: {e}")
            return []
    
    def refresh_networks(self):
        """Populate the network listbox with available networks"""
        self.network_listbox.delete(0, tk.END)
        for network in self.wifi_networks:
            security = "[S] " if network["secured"] else "[O] "
            self.network_listbox.insert(tk.END, f"{security}{network['name']} ({network['signal']})")
    
    def scan_networks(self):
        """Scan for networks and update listbox"""
        self.status_label.config(text="Scanning for networks...")
        self.root.update()
        time.sleep(1)
        
        self.wifi_networks = self.scan_wifi_networks()
        current_networks = {n["name"] for n in self.wifi_networks}
        
        new_networks = current_networks - self.previous_networks
        if new_networks:
            messagebox.showinfo("Network Available", f"New network(s) detected: {', '.join(new_networks)}")
        
        self.previous_networks = current_networks
        self.refresh_networks()
        self.status_label.config(text="Select a network to connect")
    
    def scan_networks_periodically(self):
        """Periodically scan for networks"""
        self.scan_networks()
        self.root.after(10000, self.scan_networks_periodically)
    
    def on_network_select(self, event):
        """Handle network selection"""
        if self.network_listbox.curselection():
            index = self.network_listbox.curselection()[0]
            network = self.wifi_networks[index]
            
            if network["secured"]:
                self.password_entry.config(state=tk.NORMAL)
                self.password_label.config(text="Password:")
            else:
                self.password_entry.delete(0, tk.END)
                self.password_entry.config(state=tk.DISABLED)
                self.password_label.config(text="No password required")
    
    def toggle_password_visibility(self):
        """Show or hide password"""
        self.show_password = not self.show_password
        if self.show_password:
            self.password_entry.config(show="")
            self.show_password_button.config(text="Hide")
        else:
            self.password_entry.config(show="*")
            self.show_password_button.config(text="Show")
    
    def connect_wifi(self):
        """Connect to selected WiFi network (simulated)"""
        if not self.network_listbox.curselection():
            messagebox.showwarning("Selection Required", "Please select a network to connect to.")
            return
        
        index = self.network_listbox.curselection()[0]
        network = self.wifi_networks[index]
        
        if network["secured"] and not self.password_entry.get():
            messagebox.showwarning("Password Required", "Please enter the password for this network.")
            return
        
        self.status_label.config(text=f"Connecting to {network['name']}...")
        self.root.update()
        time.sleep(1.5)
        
        self.status_label.config(text=f"Connected to {network['name']}", fg="#4CAF50")
        self.disconnect_button.config(state=tk.NORMAL)
        self.forget_button.config(state=tk.NORMAL)
    
    def disconnect_wifi(self):
        """Disconnect from current network (simulated)"""
        if not self.network_listbox.curselection():
            messagebox.showwarning("No Connection", "No active connection to disconnect.")
            return
        
        index = self.network_listbox.curselection()[0]
        network = self.wifi_networks[index]
        
        self.status_label.config(text=f"Disconnecting from {network['name']}...")
        self.root.update()
        time.sleep(1)
        
        self.status_label.config(text="Not connected", fg="#FF6B6B")
        self.disconnect_button.config(state=tk.DISABLED)
        self.forget_button.config(state=tk.DISABLED)
    
    def forget_network(self):
        """Forget the selected network (simulated)"""
        if not self.network_listbox.curselection():
            messagebox.showwarning("Selection Required", "Please select a network to forget.")
            return
        
        index = self.network_listbox.curselection()[0]
        network = self.wifi_networks[index]
        
        confirm = messagebox.askyesno("Confirm", f"Are you sure you want to forget the network '{network['name']}'?")
        if not confirm:
            return
        
        self.status_label.config(text=f"Forgetting {network['name']}...")
        self.root.update()
        time.sleep(1)
        
        self.wifi_networks.pop(index)
        self.refresh_networks()
        self.status_label.config(text="Network forgotten", fg="#FF6B6B")
        self.disconnect_button.config(state=tk.DISABLED)
        self.forget_button.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("500x600")  # Fixed size as requested
    app = WifiConnectionWindow(root)
    root.mainloop()