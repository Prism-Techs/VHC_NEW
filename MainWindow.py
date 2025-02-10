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

FONT_SIZE = 10
Font = ("Arial",30)
# HIGHT = 1
# WIDTH = 10
Font2 = ("Arial",20)
Font3 = ("Arial",30)

class mainWindow:

    def __init__(self, frame):
        self.frame = frame
        self.selectedGen = "M"
        self.selectedEye = "R" 
        
    def Load(self):
        kb = KeyBoard()
        a=50
        # time label
        #x=datetime.datetime.now () 
        self.timelabel = tk.Label (self.frame,font=Font)
        self.updateDateTime()
        self.timelabel.place(x=550, y=10)
        
        #Name amd name text
        self.Namelabel = tk.Label (self.frame,font=Font, text="Name")
        self.Namelabel.place (x=a+25, y=80)        
        self.NameText = tk.Entry (self.frame,
                             font=Font,
                             justify="left")
        self.NameText.bind ("<FocusIn>",
                       lambda event: kb.createAlphaKey(self.frame,self.NameText))
        #self.NameText.bind ("<FocusOut>",
        #                lambda event:nameTextFocusOut(NameText))               
        self.NameText.place (x=a+175,y=80)        
        self.Agelabel = tk.Label (self.frame,text="Age",font=Font)
        self.Agelabel.place (x=a+25, y=200)
        self.AgeText = tk.Entry (self.frame,font=Font, width=3)
                           
        self.AgeText.bind ("<FocusIn>", lambda event: kb.createNumaKey(self.frame,self.AgeText))
        self.AgeText.place (x=a+125, y=200)
      
      
        self.Genderlabel = tk.Label (self.frame, text="Gender",font=Font)
        self.Genderlabel.place (x=a+225, y=200)

        self.GenderSel = tk.Button (self.frame, text = 'M', width=4, font=Font2, bg="#90b2f5", command=self.genderSelected)
        self.GenderSel.place (x=a+375, y=200)
        
      
        self.Eyelabel = tk.Label (self.frame, text="Eye :",font=Font)
        self.Eyelabel.place (x=a+475, y=200)

        self.EyeSel = tk.Button (self.frame, text = 'R', width=4, font=Font2, bg="#87aaf5", command=self.eyeSelected)
        self.EyeSel.place (x=a+555, y=200) 
        # globaladc.skip_rset()
        # globaladc.main_Prepair() 
         
        def onfw():
            pageDisctonary['MainScreen'].hide()
            pageDisctonary['CffFovea'].show()  #'CffFovea'


        def onbw():
            pageDisctonary['MainScreen'].hide()
            pageDisctonary['BrkparaFovea'].show()

        fwButton = tk.Button (self.frame,
                                 text=">>", font=Font2,
                                 command=onfw, bg='#a0f291',
                                 width=10)
       
        bwButton = tk.Button (self.frame,
                                 text="<<", font=Font2,
                                 command=onbw, bg='#a0f291',
                                 width=10)
 
#         fwButton.place (x=620,y=500)
#         bwButton.place (x=420, y=500)
               #Button start the test

        def handleStart():
            CffFovea.Open ()

    def updateDateTime(self):
       raw_dt = datetime.datetime.now()
       #date_now = raw_dt.strftime("%d %b %y")
      # time_now = raw_dt.strftime("%d %b %Y %H : %M : %S %p")
       time_now = raw_dt.strftime("%d/%m/%Y %I:%M:%S %p")
      # self.timelabel.config(text = date_now)
       self.timelabel.config(text = time_now)
       self.timelabel.after(1000,self.updateDateTime)
       
    def genderSelected(self):
        if(self.GenderSel['text'] == 'M'):
            self.GenderSel['text'] = 'F'
            self.GenderSel['bg']="#f29be4"    
        else :
            self.GenderSel['text'] = 'M'
            self.GenderSel['bg']="#90b2f5"    
  
        self.selectedGen =self.GenderSel['text']
               
   
    def eyeSelected(self):
         if(self.EyeSel['text'] == 'R'):
            self.EyeSel['text'] = 'L'
            self.EyeSel['bg']='#f58787'    
         else :
            self.EyeSel['text'] = 'R'
            self.EyeSel['bg']='#87aaf5'    
  
         self.selectedEye=self.EyeSel['text']

    def show(self):        
        self.frame.place(width=1024,height=600)
        # time.sleep(1)
        globaladc.main_Prepair() # run this while loading main Screen
    
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
        # enable this

        # verify if any of the fields are missing
        if not self.AgeText.get(): valid = False
        if not self.NameText.get(): valid = False
        if not self.selectedEye : valid = False
        if not self.selectedGen : valid = False  
        if valid :
            self.loadValues()        
        return valid
    
        
        
