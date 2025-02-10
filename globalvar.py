import PatientInfo 
from dac_lib_soft import mup4728
import tkinter as tk
from tkinter import font


global pageDisctonary 
pageDisctonary = dict()

global currentPatientInfo
currentPatientInfo = PatientInfo.PatientInfo()

globaladc  = mup4728(0x61)

 

 
class CustomLabel(tk.Label):
    def __init__(self, parent, **kwargs):
        # Create custom font matching Helvetica 26
        custom_font = font.Font(
            family="Helvetica",
            size=26
        )
        
        # Default styling matching the PyQt label
        default_style = {
            'font': custom_font,
            'bg': 'black',
            'fg': 'white',
            'width': 5,  # Approximate width to match 111 pixels
            'height': 1,  # Approximate height to match 51 pixels
            'borderwidth': 2,
            'relief': 'solid',
            'justify': 'center'
        }
        
        # Update default styling with any provided kwargs
        default_style.update(kwargs)
        
        # Initialize the label with our styling
        super().__init__(parent, **default_style)
        
        # Place the label (matching QRect(580, 30, 111, 51))
        # self.place(x=700, y=30)



class CustomListbox(tk.Listbox):
    def __init__(self, parent, font_family="Helvetica", font_size=20, **kwargs):
        # Create custom font
        custom_font = font.Font(
            family=font_family,
            size=font_size
        )
        
        # Default styling
        default_style = {
            'font': custom_font,
            'width': 6,
            'bg': 'black',
            'fg': 'red',
            'selectmode': 'single',
            'selectbackground': '#3d3d3d',  # Darker grey for selection
            'selectforeground': 'red',      # Keep text red when selected
            'relief': 'solid',
            'highlightthickness': 0,        # Remove focus highlight
            'activestyle': 'none',  
            'justify': 'center',   
            "borderwidth":2                # Remove active item underline
        }
        
        # Update default styling with any provided kwargs
        default_style.update(kwargs)
        
        # Initialize the listbox with our styling
        super().__init__(parent, **default_style)
        
        # Bind events for hover effects (optional)
        self.bind('<Enter>', self.on_enter)
        self.bind('<Leave>', self.on_leave)
    
    def on_enter(self, event):
        """Optional hover effect"""
        self.configure(borderwidth=0)
    
    def on_leave(self, event):
        """Reset border on mouse leave"""
        self.configure(borderwidth=0)


