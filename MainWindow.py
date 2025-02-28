import datetime
import imp
import time
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

# Modernized constants
FONT_SIZE = 12
FONT_MAIN = ("Helvetica", 16, "bold")  # Clean, modern sans-serif font
FONT_SECONDARY = ("Helvetica", 14)     # Slightly smaller for buttons
FONT_TIME = ("Helvetica", 18, "bold")  # Larger for time display

class mainWindow:
    def __init__(self, frame):
        self.frame = frame
        self.selectedGen = "M"
        self.selectedEye = "R"
        # Set a modern background color for the frame
        self.frame.configure(bg="#f0f2f5")  # Light gray, soft modern look

    def Load(self):
        kb = KeyBoard()
        a = 50

        # Time label - sleek, centered at the top
        self.timelabel = tk.Label(self.frame, font=FONT_TIME, bg="#f0f2f5", fg="#333333")
        self.updateDateTime()
        self.timelabel.place(x=400, y=20)  # Centered horizontally

        # Name label and entry - modern styling
        self.Namelabel = tk.Label(self.frame, font=FONT_MAIN, text="Name", bg="#f0f2f5", fg="#555555")
        self.Namelabel.place(x=a + 25, y=100)        
        self.NameText = tk.Entry(self.frame, font=FONT_MAIN, justify="left", width=20, 
                                 bd=0, bg="#ffffff", fg="#333333", 
                                 highlightthickness=1, highlightcolor="#0078d4")
        self.NameText.bind("<FocusIn>", 
                          lambda event: kb.createAlphaKey(self.frame, self.NameText))
        self.NameText.place(x=a + 175, y=100)        

        # Age label and entry
        self.Agelabel = tk.Label(self.frame, text="Age", font=FONT_MAIN, bg="#f0f2f5", fg="#555555")
        self.Agelabel.place(x=a + 25, y=180)
        self.AgeText = tk.Entry(self.frame, font=FONT_MAIN, width=5, 
                                bd=0, bg="#ffffff", fg="#333333", 
                                highlightthickness=1, highlightcolor="#0078d4")
        self.AgeText.bind("<FocusIn>", 
                         lambda event: kb.createNumaKey(self.frame, self.AgeText))
        self.AgeText.place(x=a + 125, y=180)

        # Gender label and button - modern toggle button
        self.Genderlabel = tk.Label(self.frame, text="Gender", font=FONT_MAIN, bg="#f0f2f5", fg="#555555")
        self.Genderlabel.place(x=a + 225, y=180)
        self.GenderSel = tk.Button(self.frame, text="M", font=FONT_SECONDARY, width=4, 
                                   bg="#0078d4", fg="#ffffff", bd=0, 
                                   activebackground="#005bb5", command=self.genderSelected)
        self.GenderSel.place(x=a + 375, y=180)

        # Eye label and button
        self.Eyelabel = tk.Label(self.frame, text="Eye:", font=FONT_MAIN, bg="#f0f2f5", fg="#555555")
        self.Eyelabel.place(x=a + 475, y=180)
        self.EyeSel = tk.Button(self.frame, text="R", font=FONT_SECONDARY, width=4, 
                                bg="#0078d4", fg="#ffffff", bd=0, 
                                activebackground="#005bb5", command=self.eyeSelected)
        self.EyeSel.place(x=a + 555, y=180)

        # Navigation buttons - modern flat design
        def onfw():
            pageDisctonary['MainScreen'].hide()
            pageDisctonary['CffFovea'].show()

        def onbw():
            pageDisctonary['MainScreen'].hide()
            pageDisctonary['BrkparaFovea'].show()

        fwButton = tk.Button(self.frame, text=">>", font=FONT_SECONDARY, 
                             command=onfw, bg="#28a745", fg="#ffffff", 
                             bd=0, activebackground="#218838", width=10)
        bwButton = tk.Button(self.frame, text="<<", font=FONT_SECONDARY, 
                             command=onbw, bg="#28a745", fg="#ffffff", 
                             bd=0, activebackground="#218838", width=10)
        fwButton.place(x=620, y=500)
        bwButton.place(x=420, y=500)

        # Start test function (unchanged)
        def handleStart():
            CffFovea.Open()

    def updateDateTime(self):
        raw_dt = datetime.datetime.now()
        time_now = raw_dt.strftime("%d/%m/%Y %I:%M:%S %p")
        self.timelabel.config(text=time_now)
        self.timelabel.after(1000, self.updateDateTime)

    def genderSelected(self):
        if self.GenderSel['text'] == 'M':
            self.GenderSel['text'] = 'F'
            self.GenderSel['bg'] = "#e83e8c"  # Pink for female
            self.GenderSel['activebackground'] = "#c9307a"
        else:
            self.GenderSel['text'] = 'M'
            self.GenderSel['bg'] = "#0078d4"  # Blue for male
            self.GenderSel['activebackground'] = "#005bb5"
        self.selectedGen = self.GenderSel['text']

    def eyeSelected(self):
        if self.EyeSel['text'] == 'R':
            self.EyeSel['text'] = 'L'
            self.EyeSel['bg'] = "#dc3545"  # Red for left
            self.EyeSel['activebackground'] = "#bd2130"
        else:
            self.EyeSel['text'] = 'R'
            self.EyeSel['bg'] = "#0078d4"  # Blue for right
            self.EyeSel['activebackground'] = "#005bb5"
        self.selectedEye = self.EyeSel['text']

    def show(self):        
        self.frame.place(width=1024, height=600)
        globaladc.main_Prepair()

    def hide(self):
        self.frame.place_forget()

    def getName():
        return "MainScreen"    

    def loadValues(self):
        currentPatientInfo.Age = self.AgeText.get()
        currentPatientInfo.Name = self.NameText.get()
        currentPatientInfo.eye = self.selectedEye
        currentPatientInfo.Gender = self.selectedGen
        currentPatientInfo.date = self.timelabel.cget("text")

    def ValidateUserInput(self):
        valid = True
        if not self.AgeText.get(): valid = False
        if not self.NameText.get(): valid = False
        if not self.selectedEye: valid = False
        if not self.selectedGen: valid = False  
        if valid:
            self.loadValues()        
        return valid
