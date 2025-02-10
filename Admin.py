import tkinter as tk
from tkinter import Frame, ttk
from Keyboard import KeyBoard
from FlikerScreen import flikerWindow
from CFF_FOVEA import CffFovea
from globalvar import pageDisctonary
from globalvar import currentPatientInfo
from Splash import Splash
from globalvar import globaladc
import tkinter.font as tkfont

FONT_SIZE = 10
Font = ("Arial",30)
HIGHT = 1
WIDTH = 10
Font2 = ("Arial",20)
Font3 = ("Arial",30)

class Admin:

    def __init__(self, frame):
        self.frame = frame
        
    def Load(self):
        kb = KeyBoard()
        
        #Name amd name text
        self.Namelabel = tk.Label (self.frame,font=Font, text="Password")
        self.Namelabel.place (x=10, y=80)
        
        self.Password = tk.Entry (self.frame,
                             font=Font,
                             justify="left")
        self.Password.config(show="*")
        self.Password.bind ("<FocusIn>",
                       lambda event: kb.createNumaKey(self.frame,self.NameText))
        self.Password.place(x=220,y=80)               
    def show(self):
        self.frame.place(width=1024,height=600)

    def hide(self):
        self.frame.place_forget()

