import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import json
import os
from PIL import Image, ImageTk
from header import HeaderComponent
from Startupclass import StatrupClass
from functools import lru_cache
import gc

class HomePage:
    def __init__(self, root):
        # Enable garbage collection for better memory management
        gc.enable()
        
        # Initialize all instance variables first
        self.root = root
        self.wifi_window = None
        self.time_label = None
        self.date_label = None
        self.user_info_label = None
        self.buttons = []
        # Reduced update frequency to save CPU
        self.time_update_interval = 30000  # 30 seconds
        self.user_data_cache = None
        self.last_cache_update = 0
        self.cache_lifetime = 60000  # 1 minute
        
        # Pre-define colors and fonts to reduce object creation
        self.colors = {
            'bg_black': 'black',
            'fg_white': 'white',
            'button_normal': '#101826',
            'button_hover': '#2196F3',
            'button_hover_fg': '#64B5F6'
        }
        
        self.fonts = {
            'welcome': ('Helvetica Neue', 14, 'bold'),
            'datetime': ('Helvetica Neue', 10),
            'button': ('Arial', 24, 'bold')
        }
        
        # Setup window properties
        self.root.geometry("1024x600")
        self.root.resizable(False, False)
        self.root.configure(bg=self.colors['bg_black'])
        self.root.overrideredirect(True)
        
        # Reduce window manager updates
        self.root.update_idletasks()
        
        # Initialize the UI
        self.setup_ui()
        
        # Schedule periodic garbage collection
        self.schedule_gc()

    def schedule_gc(self):
        """Schedule periodic garbage collection"""
        gc.collect()
        self.root.after(300000, self.schedule_gc)  # Run every 5 minutes

    def setup_ui(self):
        # Add the header component
        self.header = HeaderComponent(self.root, "                                                    Home Page")
        self.header.set_wifi_callback(self.open_wifi_page)
        
        # Welcome Label (User Info)
        self.user_info_label = tk.Label(
            self.root,
            text="Welcome",
            font=self.fonts['welcome'],
            fg=self.colors['fg_white'],
            bg=self.colors['bg_black'],
            anchor='w'
        )
        self.user_info_label.place(x=20, y=150, width=280, height=40)
        
        # Create main buttons
        self.create_buttons()
        
        # Time and Date Labels using same configuration
        label_config = {
            'font': self.fonts['datetime'],
            'fg': self.colors['fg_white'],
            'bg': self.colors['bg_black']
        }
        
        self.time_label = tk.Label(self.root, **label_config)
        self.time_label.place(x=960, y=550)
        
        self.date_label = tk.Label(self.root, **label_config)
        self.date_label.place(x=934, y=570)
        
        # Initialize time display
        self._update_initial_datetime()
        
        # Check user role
        self.check_user_role()

    def _update_initial_datetime(self):
        """Initial datetime update with current time"""
        current = datetime.now()
        self.time_label.config(text=current.strftime('%H:%M'))
        self.date_label.config(text=current.strftime('%d-%m-%Y'))
        self.root.after(self.time_update_interval, self.update_datetime)

    @lru_cache(maxsize=32)
    def get_button_config(self, state='normal'):
        """Cache button configurations"""
        if state == 'normal':
            return {
                'font': self.fonts['button'],
                'bg': self.colors['button_normal'],
                'fg': self.colors['fg_white'],
                'bd': 1,
                'relief': 'solid',
                'width': 15,
                'height': 1
            }
        return {
            'bg': self.colors['button_hover'],
            'fg': self.colors['button_hover_fg'],
            'bd': 2
        }

    def create_buttons(self):
        """Create all main buttons with proper styling"""
        button_configs = [
            ("Create User", 347, 150, self.create_user),
            ("View Reports", 347, 280, self.view_reports),
            ("Test Mode", 347, 410, self.test_mode)
        ]
        
        for text, x, y, command in button_configs:
            button = tk.Button(
                self.root,
                text=text,
                command=command,
                **self.get_button_config()
            )
            button.place(x=x, y=y)
            
            # Use method references instead of lambdas for better memory usage
            button.bind('<Enter>', lambda e, b=button: self.on_button_hover(b))
            button.bind('<Leave>', lambda e, b=button: self.on_button_leave(b))
            
            self.buttons.append(button)

    def on_button_hover(self, button):
        """Handle button hover with compatible color values"""
        button.configure(**self.get_button_config('hover'))

    def on_button_leave(self, button):
        """Handle button leave event"""
        button.configure(**self.get_button_config('normal'))

    @lru_cache(maxsize=1)
    def get_user_data_path(self):
        """Cache the user data file path"""
        return os.path.join(os.path.dirname(os.path.realpath(__file__)), 
                           "user_data", "latest_user.json")

    def check_user_role(self):
        """Check user role and update UI accordingly"""
        try:
            json_path = self.get_user_data_path()
            
            if os.path.exists(json_path):
                with open(json_path, 'r') as file:
                    user_data = json.load(file)
                
                is_operator = user_data.get('is_operator', 0) == 1
                self.update_user_info(user_data)
                self.update_button_visibility(is_operator)
            else:
                messagebox.showwarning('Error', 'No user data found. Please log in again.')
                
        except Exception as e:
            messagebox.showerror('Error', f'Error loading user data: {str(e)}')

    def update_user_info(self, user_data):
        """Update user info label"""
        title = user_data.get('title', '')
        name = f"{user_data.get('first_name', '')} {user_data.get('last_name', '')}"
        user_info = f"Welcome,\n{title} {name}" if title else f"Welcome,\n{name}"
        self.user_info_label.config(text=user_info)

    def update_datetime(self):
        """Update time and date labels"""
        current = datetime.now()
        self.time_label.config(text=current.strftime('%H:%M'))
        self.date_label.config(text=current.strftime('%d-%m-%Y'))
        self.root.after(self.time_update_interval, self.update_datetime)

    def open_wifi_page(self):
        """Open WiFi settings window"""
        if not self.wifi_window:  # Prevent multiple windows
            print("Opening WiFi page")

    def create_user(self):
        """Handle create user button click"""
        print("Create user clicked")

    def view_reports(self):
        """Handle view reports button click"""
        print("View reports clicked")

    def test_mode(self):
        """Handle test mode button click"""
        self.root.withdraw()
        st = StatrupClass()
        st.main()

def main():
    # Set process priority (if possible)
    try:
        os.nice(10)
    except AttributeError:
        pass
    
    root = tk.Tk()
    
    # Optimize for performance
    root.update_idletasks()
    
    app = HomePage(root)
    root.mainloop()

if __name__ == "__main__":
    main()