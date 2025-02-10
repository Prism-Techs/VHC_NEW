import tkinter as tk
from PIL import Image, ImageTk
from tkinter import font
import os

class HeaderComponent:
    def __init__(self, parent_frame, page_title=""):
            # Create header frame
            self.header_frame = tk.Frame(parent_frame, bg='#1f2836', height=41)
            self.header_frame.pack(fill='x')
            
            # Keep reference of the image to prevent garbage collection
            self.images = {}
            
            # Get current directory and construct absolute paths
            current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            logo_path = os.path.join(current_dir,"UI" , "logo.png")
            wifi_path = os.path.join(current_dir, "UI", "wifi_logo.png")
            
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
                self.logo_label.place(x=0, y=10)
            except Exception as e:
                print(f"Logo image not found: {e}")
                print(f"Attempted path: {logo_path}")
                
            # Setup WiFi icon
            self.wifi_label = self.create_clickable_label(
                self.header_frame,
                bg='#1f2836'
            )
            self.wifi_label.place(x=868, y=5)



             # Company name label
            tk.Label(
                self.header_frame,
                text="Vekaria Healthcare",
                font=('Helvetica Neue', 16, 'bold'),
                bg='#1f2836',
                fg='white'
            ).place(x=60, y=10)
            
            # Version label
            tk.Label(
                self.header_frame,
                text="V1.0",
                font=('Helvetica Neue', 14, 'bold'),
                bg='#1f2836',
                fg='white'
            ).place(x=930, y=10)
            
            # Page title
            self.title_label = None
            if page_title:
                self.title_label = tk.Label(
                    parent_frame,
                    text=page_title,
                    font=("Arial", 20),
                    bg='black',
                    fg='white'
                )
                self.title_label.place(x=0, y=40)

            
            try:
                wifi_image = Image.open(wifi_path)
                wifi_image = wifi_image.resize((41, 31), Image.LANCZOS)
                self.images['wifi'] = ImageTk.PhotoImage(wifi_image)
                self.wifi_label.configure(image=self.images['wifi'])
            except Exception as e:
                print(f"WiFi logo not found: {e}")
                print(f"Attempted path: {wifi_path}")
                self.wifi_label.configure(text="WiFi", fg='white')

    def create_clickable_label(self, master, **kwargs):
        """Create a clickable label with callback functionality"""
        label = tk.Label(master, **kwargs)
        label.bind('<Button-1>', self._on_click)
        label.callback = None
        return label

    def _on_click(self, event):
        """Handle click events on labels"""
        if hasattr(event.widget, 'callback') and event.widget.callback:
            event.widget.callback()

    def set_wifi_callback(self, callback):
        """Set callback for wifi icon click"""
        if hasattr(self, 'wifi_label'):
            self.wifi_label.callback = callback