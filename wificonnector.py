import tkinter as tk
from tkinter import ttk, messagebox
import time

class WifiConnectionWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Vekaria Healthcare - WiFi Connection")
        self.root.configure(bg="#1F2937")
        
        # Colors for dark theme
        self.bg_color = "#1F2937"  # Dark blue-gray background
        self.text_color = "#FFFFFF"  # White text
        self.button_bg = "#000000"  # Black button
        self.button_fg = "#FFFFFF"  # White text on button
        self.button_active_bg = "#333333"  # Dark gray when button pressed
        self.entry_bg = "#2C3E50"  # Slightly lighter than background
        self.border_color = "#4B5563"  # Medium gray for borders
        self.list_bg = "#2C3E50"  # Same as entry
        
        # Fonts
        self.title_font = ("Arial", 16, "bold")
        self.normal_font = ("Arial", 12)
        self.button_font = ("Arial", 12)
        
        self.create_header()
        self.create_content()
        
        # Mock data for demo
        self.wifi_networks = [
            {"name": "Hospital_WiFi", "signal": "Strong", "secured": True},
            {"name": "Staff_Network", "signal": "Strong", "secured": True},
            {"name": "Guest_Network", "signal": "Medium", "secured": False},
            {"name": "Vekaria_5G", "signal": "Strong", "secured": True},
            {"name": "Medical_Devices", "signal": "Weak", "secured": True}
        ]
        
        # Populate network listbox
        self.refresh_networks()
        
    def create_header(self):
        """Create the header with logo and title"""
        self.header_frame = tk.Frame(self.root, bg="#000000", height=40)
        self.header_frame.pack(fill=tk.X)
        
        # Logo text (or you can use an image)
        self.logo_label = tk.Label(self.header_frame, text="Vekaria Healthcare", 
                                  font=("Arial", 14, "bold"), fg="#FFFFFF", bg="#000000")
        self.logo_label.pack(side=tk.LEFT, padx=10)
        
        # Version number
        self.version_label = tk.Label(self.header_frame, text="V1.0", 
                                     font=("Arial", 12), fg="#FFFFFF", bg="#000000")
        self.version_label.pack(side=tk.RIGHT, padx=10)
        
        # WiFi icon (text representation)
        self.wifi_icon = tk.Label(self.header_frame, text="WiFi", 
                                 font=("Arial", 12), fg="#FFFFFF", bg="#000000")
        self.wifi_icon.pack(side=tk.RIGHT, padx=5)
        
    def create_content(self):
        """Create the main content area"""
        self.content_frame = tk.Frame(self.root, bg=self.bg_color)
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        self.title_label = tk.Label(self.content_frame, text="WiFi Connection", 
                                   font=self.title_font, bg=self.bg_color, fg=self.text_color)
        self.title_label.pack(pady=(0, 20))
        
        # Network section
        self.network_frame = tk.Frame(self.content_frame, bg=self.bg_color)
        self.network_frame.pack(fill=tk.X, pady=10)
        
        self.network_label = tk.Label(self.network_frame, text="Available Networks", 
                                     font=self.normal_font, bg=self.bg_color, fg=self.text_color)
        self.network_label.pack(anchor="w")
        
        # Network listbox with scrollbar
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
                                        height=6,
                                        bd=1,
                                        highlightthickness=1,
                                        highlightbackground=self.border_color)
        self.network_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Connect scrollbar to listbox
        self.scrollbar.config(command=self.network_listbox.yview)
        self.network_listbox.config(yscrollcommand=self.scrollbar.set)
        
        # Bind selection event
        self.network_listbox.bind("<<ListboxSelect>>", self.on_network_select)
        
        # Button frame for scan/rescan
        self.scan_button_frame = tk.Frame(self.content_frame, bg=self.bg_color)
        self.scan_button_frame.pack(fill=tk.X, pady=10)
        
        self.scan_button = self.create_button(self.scan_button_frame, "Scan Networks", self.scan_networks)
        self.scan_button.pack(side=tk.LEFT, padx=5)
        
        self.rescan_button = self.create_button(self.scan_button_frame, "Refresh", self.scan_networks)
        self.rescan_button.pack(side=tk.LEFT, padx=5)
        
        # Password frame
        self.password_frame = tk.Frame(self.content_frame, bg=self.bg_color)
        self.password_frame.pack(fill=tk.X, pady=10)
        
        self.password_label = tk.Label(self.password_frame, text="Password:", 
                                      font=self.normal_font, bg=self.bg_color, fg=self.text_color)
        self.password_label.pack(side=tk.LEFT, padx=(0, 10))
        
        self.password_entry = tk.Entry(self.password_frame, 
                                      bg=self.entry_bg, 
                                      fg=self.text_color,
                                      font=self.normal_font,
                                      show="•",
                                      bd=1,
                                      highlightthickness=1,
                                      highlightbackground=self.border_color)
        self.password_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Show/hide password button
        self.show_password = False
        self.show_password_button = self.create_button(self.password_frame, "Show", self.toggle_password_visibility)
        self.show_password_button.pack(side=tk.RIGHT, padx=5)
        
        # Connection options
        self.options_frame = tk.Frame(self.content_frame, bg=self.bg_color)
        self.options_frame.pack(fill=tk.X, pady=10)
        
        self.connect_button = self.create_button(self.options_frame, "Connect", self.connect_wifi)
        self.connect_button.pack(side=tk.LEFT, padx=5)
        
        self.disconnect_button = self.create_button(self.options_frame, "Disconnect", self.disconnect_wifi)
        self.disconnect_button.pack(side=tk.LEFT, padx=5)
        
        self.forget_button = self.create_button(self.options_frame, "Forget Network", self.forget_network)
        self.forget_button.pack(side=tk.LEFT, padx=5)
        
        # Status label
        self.status_label = tk.Label(self.content_frame, 
                                    text="Not connected", 
                                    font=self.normal_font, 
                                    bg=self.bg_color, 
                                    fg="#FF6B6B")  # Red text for not connected
        self.status_label.pack(pady=10)
        
        # Initially disable disconnect and forget buttons
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
    
    def refresh_networks(self):
        """Populate the network listbox with available networks"""
        self.network_listbox.delete(0, tk.END)
        for network in self.wifi_networks:
            security = "🔒 " if network["secured"] else "🔓 "
            signal_strength = "📶" if network["signal"] == "Strong" else ("📶" if network["signal"] == "Medium" else "📶")
            self.network_listbox.insert(tk.END, f"{security}{network['name']} ({signal_strength})")
    
    def scan_networks(self):
        """Simulate scanning for networks"""
        self.status_label.config(text="Scanning for networks...")
        
        # Show scanning animation
        self.root.update()
        time.sleep(1)  # Simulate scanning delay
        
        self.refresh_networks()
        self.status_label.config(text="Select a network to connect")
    
    def on_network_select(self, event):
        """Handle network selection"""
        if self.network_listbox.curselection():
            index = self.network_listbox.curselection()[0]
            network = self.wifi_networks[index]
            
            # Enable/disable password field based on security
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
            self.password_entry.config(show="•")
            self.show_password_button.config(text="Show")
    
    def connect_wifi(self):
        """Connect to selected WiFi network"""
        if not self.network_listbox.curselection():
            messagebox.showwarning("Selection Required", "Please select a network to connect to.")
            return
        
        index = self.network_listbox.curselection()[0]
        network = self.wifi_networks[index]
        
        if network["secured"] and not self.password_entry.get():
            messagebox.showwarning("Password Required", "Please enter the password for this network.")
            return
        
        # Simulate connection process
        self.status_label.config(text=f"Connecting to {network['name']}...")
        self.root.update()
        time.sleep(1.5)  # Simulate connection delay
        
        # Show success
        self.status_label.config(text=f"Connected to {network['name']}", fg="#4CAF50")  # Green for connected
        
        # Enable disconnect and forget buttons
        self.disconnect_button.config(state=tk.NORMAL)
        self.forget_button.config(state=tk.NORMAL)
    
    def disconnect_wifi(self):
        """Disconnect from current network"""
        if not self.network_listbox.curselection():
            messagebox.showwarning("No Connection", "No active connection to disconnect.")
            return
        
        index = self.network_listbox.curselection()[0]
        network = self.wifi_networks[index]
        
        # Simulate disconnection
        self.status_label.config(text=f"Disconnecting from {network['name']}...")
        self.root.update()
        time.sleep(1)  # Simulate disconnection delay
        
        # Update status
        self.status_label.config(text="Not connected", fg="#FF6B6B")
        
        # Disable buttons
        self.disconnect_button.config(state=tk.DISABLED)
        self.forget_button.config(state=tk.DISABLED)
    
    def forget_network(self):
        """Forget the selected network"""
        if not self.network_listbox.curselection():
            messagebox.showwarning("Selection Required", "Please select a network to forget.")
            return
        
        index = self.network_listbox.curselection()[0]
        network = self.wifi_networks[index]
        
        # Confirm before forgetting
        confirm = messagebox.askyesno("Confirm", f"Are you sure you want to forget the network '{network['name']}'?")
        if not confirm:
            return
        
        # Simulate forgetting
        self.status_label.config(text=f"Forgetting {network['name']}...")
        self.root.update()
        time.sleep(1)  # Simulate delay
        
        # Remove from list (in a real app, would remove from saved networks)
        self.wifi_networks.pop(index)
        self.refresh_networks()
        
        # Update status
        self.status_label.config(text="Network forgotten", fg="#FF6B6B")
        
        # Disable buttons
        self.disconnect_button.config(state=tk.DISABLED)
        self.forget_button.config(state=tk.DISABLED)

# Demo code for testing the window
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("500x600")
    app = WifiConnectionWindow(root)
    root.mainloop()