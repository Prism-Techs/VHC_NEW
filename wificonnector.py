import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import time
import re
from PIL import Image, ImageTk
import os
# from Keyboard import KeyBoard  # Import KeyBoard from keyboard.py
from globalvar import globaladc  # Assuming this is available


import tkinter as tk
from globalvar import globaladc

class KeyBoard:
    def __init__(self):
        self.shift_active = False
        self._drag_data = {"x": 0, "y": 0, "width": 0, "height": 0}  # For dragging and resizing
        self.current_window = None  # Track current keyboard window
        self.current_entry = None  # Track current entry
        self.resizing = False  # Flag to indicate resize mode

    def cleanup_keyboard(self):
        if self.current_window and self.current_window.winfo_exists():
            try:
                self.current_window.destroy()
                self.current_window = None
                self.current_entry = None
            except tk.TclError:
                self.current_window = None
                self.current_entry = None

    def on_drag_start(self, event, window):
        """Begin drag of the window"""
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y

    def on_resize_start(self, event, window):
        """Begin resize of the window with Ctrl key"""
        if event.state & 0x4:  # Check if Ctrl key is pressed (state & 0x4)
            self.resizing = True
            self._drag_data["x"] = event.x
            self._drag_data["y"] = event.y
            self._drag_data["width"] = window.winfo_width()
            self._drag_data["height"] = window.winfo_height()

    def on_drag_motion(self, event, window):
        """Handle dragging of the window"""
        if window.winfo_exists() and not self.resizing:  # Only drag if not resizing
            delta_x = event.x - self._drag_data["x"]
            delta_y = event.y - self._drag_data["y"]
            x = window.winfo_x() + delta_x
            y = window.winfo_y() + delta_y
            window.geometry(f"+{x}+{y}")
            window.lift()  # Keep window on top while dragging

    def on_resize_motion(self, event, window):
        """Handle resizing of the window with Ctrl key"""
        if window.winfo_exists() and self.resizing and (event.state & 0x4):  # Check Ctrl key
            delta_x = event.x - self._drag_data["x"]
            delta_y = event.y - self._drag_data["y"]
            new_width = max(400, self._drag_data["width"] + delta_x)  # Minimum width 400
            new_height = max(150, self._drag_data["height"] + delta_y)  # Minimum height 150
            window.geometry(f"{int(new_width)}x{int(new_height)}+{window.winfo_x()}+{window.winfo_y()}")
            window.lift()  # Keep window on top while resizing

    def on_release(self, event, window):
        """End resize or drag mode"""
        self.resizing = False

    def select(self, entry, window, mainwindow, value, ucase=None):
        """Handle key selection and input"""
        if not window.winfo_exists():  # Check if window still exists
            return

        uppercase = ucase

        if value == "Space":
            value = ' '
        elif value == 'Enter':
            value = ''
            globaladc.get_print("enter pressed")
            mainwindow.focus_force()  # Return focus to the main window
            self.cleanup_keyboard()
            return
        elif value == 'Tab':
            value = '\t'

        if value == "Back" or value == '<-':
            if isinstance(entry, tk.Entry):
                if len(entry.get()) > 0:
                    entry.delete(len(entry.get()) - 1, 'end')
            else:
                entry.delete('end - 2c', 'end')

        elif value == 'Shift ^':
            self.shift_active = not self.shift_active
            for widget in window.winfo_children():
                if isinstance(widget, tk.Frame):
                    for btn in widget.winfo_children():
                        if isinstance(btn, tk.Button) and btn['text'] not in ['Space', 'Enter', 'Back', 'Shift', '<-']:
                            btn['text'] = btn['text'].upper() if self.shift_active else btn['text'].lower()

        elif value not in ('Caps Lock', 'Shift'):
            if self.shift_active:
                value = value.upper()
            entry.insert('end', value)
            entry.icursor('end')  # Move cursor to end
            entry.focus_set()  # Ensure focus stays on the entry
            window.lift()  # Keep keyboard on top

        globaladc.buzzer_1()
        window.lift()  # Keep keyboard on top after each action

    def createAlphaKey(self, root, entry, number=False):
        """Create alphabetic keyboard"""
        # Don't recreate keyboard if it's already showing for this entry
        if self.current_window and self.current_window.winfo_exists() and self.current_entry == entry:
            self.current_window.lift()
            return self.current_window

        self.cleanup_keyboard()
        self.current_entry = entry

        alphabets = [
            ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '@'],
            ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '#'],
            ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', '-', '*'],
            ['Shift ^', 'z', 'x', 'c', 'v', 'b', 'n', 'm', '!', 'Back'],
            ['Space', 'Enter']
        ]

        window = tk.Toplevel(root)
        window.attributes('-topmost', True)  # Make window stay on top
        self.current_window = window

        x = root.winfo_x()
        y = root.winfo_y()

        window.geometry("+%d+%d" % (x + 20, y + 400))
        window.overrideredirect(1)  # Keep borderless for dragging
        window.configure(background="black")
        window.wm_attributes("-alpha", 0.7)

        # Add dragging and resizing bindings
        window.bind("<Button-1>", lambda e: self.on_drag_start(e, window))
        window.bind("<B1-Motion>", lambda e: self.on_drag_motion(e, window))
        window.bind("<Control-Button-1>", lambda e: self.on_resize_start(e, window))
        window.bind("<Control-B1-Motion>", lambda e: self.on_resize_motion(e, window))
        window.bind("<ButtonRelease-1>", lambda e: self.on_release(e, window))

        # Create main frame
        main_frame = tk.Frame(window, bg='black')
        main_frame.pack(padx=2, pady=2)

        button_style = {
            'bg': "black",
            'fg': "white",
            'padx': 2,
            'pady': 2,
            'font': ('Arial', 12),
            'bd': 1
        }

        for y, row in enumerate(alphabets):
            x = 0
            for text in row:
                if text == 'Shift':
                    width = 8
                    columnspan = 2
                elif text == 'Space':
                    width = 40
                    columnspan = 8
                elif text == 'Enter':
                    width = 8
                    columnspan = 2
                elif text == 'Back':
                    width = 8
                    columnspan = 2
                else:
                    width = 5
                    columnspan = 1

                button = tk.Button(
                    main_frame,
                    text=text,
                    width=width,
                    command=lambda value=text: self.select(entry, window, root, value),
                    **button_style
                )
                button.grid(row=y, column=x, columnspan=columnspan, padx=2, pady=2, sticky='nsew')
                button.bind("<Button-1>", lambda e, w=window: self.on_drag_start(e, w))
                button.bind("<B1-Motion>", lambda e, w=window: self.on_drag_motion(e, w))
                button.bind("<Control-Button-1>", lambda e, w=window: self.on_resize_start(e, w))
                button.bind("<Control-B1-Motion>", lambda e, w=window: self.on_resize_motion(e, w))
                button.bind("<ButtonRelease-1>", lambda e, w=window: self.on_release(e, w))

                x += columnspan

        window.update_idletasks()  # Ensure window is fully created
        window.lift()  # Raise window to top
        entry.focus_set()  # Keep focus on entry
        return window

    def createNumaKey(self, root, entry, number=False):
        """Create numeric keyboard"""
        self.cleanup_keyboard()

        numbers = [
            ['1', '2', '3'],
            ['4', '5', '6'],
            ['7', '8', '9'],
            ['0', 'Enter', '<-']
        ]

        window = tk.Toplevel(root)
        window.attributes('-topmost', True)  # Make window stay on top
        self.current_window = window

        x = root.winfo_x()
        y = root.winfo_y()

        window.geometry("+%d+%d" % (x + 40, y + 300))
        window.overrideredirect(1)  # Keep borderless for dragging
        window.configure(background="cornflowerblue")
        window.wm_attributes("-alpha", 0.7)

        # Add dragging and resizing bindings
        window.bind("<Button-1>", lambda e: self.on_drag_start(e, window))
        window.bind("<B1-Motion>", lambda e: self.on_drag_motion(e, window))
        window.bind("<Control-Button-1>", lambda e: self.on_resize_start(e, window))
        window.bind("<Control-B1-Motion>", lambda e: self.on_resize_motion(e, window))
        window.bind("<ButtonRelease-1>", lambda e: self.on_release(e, window))

        button_style = {
            'width': 10,
            'padx': 3,
            'pady': 3,
            'bd': 12,
            'bg': "black",
            'fg': "white"
        }

        for y, row in enumerate(numbers):
            for x, text in enumerate(row):
                button = tk.Button(
                    window,
                    text=text,
                    command=lambda value=text: self.select(entry, window, root, value),
                    **button_style
                )
                button.grid(row=y, column=x, padx=2, pady=2, sticky='nsew')
                button.bind("<Button-1>", lambda e, w=window: self.on_drag_start(e, w))
                button.bind("<B1-Motion>", lambda e, w=window: self.on_drag_motion(e, w))
                button.bind("<Control-Button-1>", lambda e, w=window: self.on_resize_start(e, w))
                button.bind("<Control-B1-Motion>", lambda e, w=window: self.on_resize_motion(e, w))
                button.bind("<ButtonRelease-1>", lambda e, w=window: self.on_release(e, w))

        window.update_idletasks()  # Ensure window is fully created
        window.lift()  # Raise window to top
        entry.focus_set()  # Keep focus on entry
        return window


import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import time
import re
from PIL import Image, ImageTk
import os
from Keyboard import KeyBoard  # Import KeyBoard from keyboard.py
from globalvar import globaladc  # Assuming this is available

class WifiConnectionWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Vekaria Healthcare - WiFi Connection")
        self.configure(bg="#1F2937")
        self.parent = parent  # Store parent for reference
        
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
        
        # Initialize the keyboard
        self.keyboard = KeyBoard()
        
        self.create_header()
        self.create_content()
        
        # Store previously detected networks to check for new ones
        self.previous_networks = set()
        self.wifi_networks = []
        
        # Scan networks once at startup
        self.scan_networks()
        self.transient(parent)  # Make it modal if desired
        self.grab_set()  # Focus on this window
        self.protocol("WM_DELETE_WINDOW", self.on_close)  # Handle window close

    def on_close(self):
        """Handle window close event"""
        self.keyboard.cleanup_keyboard()  # Clean up keyboard on close
        self.grab_release()
        self.destroy()

    def create_header(self):
        """Create the header with logo, company name, version, and title"""
        self.header_frame = tk.Frame(self, bg='#1f2836', height=41)
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
            self.logo_label.place(x=10, y=9)
        except Exception as e:
            print(f"Logo image not found: {e}")
            print(f"Attempted path: {logo_path}")
        
        # Company name label
        tk.Label(
            self.header_frame,
            text="Vekaria Healthcare",
            font=('Helvetica Neue', 14, 'bold'),
            bg='#1f2836',
            fg='white'
        ).place(x=60, y=10)
        
        # Version label
        tk.Label(
            self.header_frame,
            text="V1.0",
            font=('Helvetica Neue', 12, 'bold'),
            bg='#1f2836',
            fg='white'
        ).place(x=450, y=12)
        
        # Page title
        self.title_label = tk.Label(
            self,
            text="WiFi Page",
            font=("Arial", 18),
            bg='#1f2836',
            fg='white'
        )
        self.title_label.place(x=10, y=41)

    def create_content(self):
        """Create the main content area"""
        self.content_frame = tk.Frame(self, bg=self.bg_color)
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(70, 20))
        
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
                                        height=8,
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
        
        # Bind click to open keyboard and focus out to clean up
        self.password_entry.bind("<FocusIn>", self.show_keyboard)
        self.password_entry.bind("<FocusOut>", lambda event: self.keyboard.cleanup_keyboard())
        
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

    def show_keyboard(self, event):
        """Show the on-screen keyboard for the password entry"""
        if self.password_entry['state'] == tk.NORMAL:
            print("Attempting to show keyboard")  # Debug print
            try:
                # Use the Toplevel window as the root for keyboard
                self.keyboard.createAlphaKey(self, self.password_entry)
                print("Keyboard created successfully with Toplevel")  # Debug print
                self.password_entry.focus_set()  # Ensure focus is on the entry
            except Exception as e:
                print(f"Error creating keyboard with Toplevel: {e}")  # Debug error
                try:
                    # Fallback: Use the parent (root) window
                    self.keyboard.createAlphaKey(self.parent, self.password_entry)
                    print("Keyboard created successfully with parent")  # Debug print
                    self.password_entry.focus_set()
                except Exception as e:
                    print(f"Error creating keyboard with parent: {e}")  # Debug error

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
        self.update()
        time.sleep(1)
        
        self.wifi_networks = self.scan_wifi_networks()
        current_networks = {n["name"] for n in self.wifi_networks}
        
        new_networks = current_networks - self.previous_networks
        if new_networks:
            messagebox.showinfo("Network Available", f"New network(s) detected: {', '.join(new_networks)}")
        
        self.previous_networks = current_networks
        self.refresh_networks()
        self.status_label.config(text="Select a network to connect")

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
        self.update()
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
        self.update()
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
        self.update()
        time.sleep(1)
        
        self.wifi_networks.pop(index)
        self.refresh_networks()
        self.status_label.config(text="Network forgotten", fg="#FF6B6B")
        self.disconnect_button.config(state=tk.DISABLED)
        self.forget_button.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("500x600")
    app = WifiConnectionWindow(root)
    root.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("500x600")
    app = WifiConnectionWindow(root)
    root.mainloop()