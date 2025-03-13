import datetime
import os
import tkinter as tk
from tkinter import IntVar, PhotoImage, ttk
#from schedule import Scheduler, every, repeat, run_pending
import PerodicThread
import time
import threading
#import schedule
# from globalvar import pageDisctonary
# from globalvar import globaladc
from header import HeaderComponent


Font = ("Arial",20)

Text_Fliker_OFF = "Fliker is Off Press to Change"
Text_Fliker_ON = "Fliker is On Press to Change"
flikerOn = False
defaultdepth = 7
maxdepth = 15
# intervel = globaladc.get_flicker_delay()    #0.044 #sec
intervel = 10    #0.044 #sec
Font2 = ("Arial",20)


def HandleFliker(param):
    # add code here to run whin fliker is swtched on/off
    return

class flikerWindow:
    #init call
    def __init__(self, frame):
        self.fliker_bool = True               
        self.frame = frame
        self.content_frame = tk.Frame(self.frame, bg='#1f2836')
        self.label_frame = tk.LabelFrame(self.content_frame, text = 'Depth',height=250, width=200, bg='white')
        self.label_frame.place(x="40", y="40")
        self.depthVal = tk.IntVar()
        self.depthVal.set(defaultdepth)  
        self.threadCreated =False
        self.header = HeaderComponent(frame,"Macular Densitometer                                                        Flicker Demo")
        


        
        def UpButtonClicked():
            y = self.depthVal.get()
            if(y < maxdepth):
                x = y+1
                self.depthVal.set(x)
            #globaladc.buzzer_1()
              
        def DownButtonClicked():
            if(self.depthVal.get() > 0):
                x= self.depthVal.get()-1
                self.depthVal.set(x)
            #globaladc.buzzer_1()
             
        self.UPButton = tk.Button (self.content_frame,
                                  text="+",  
                                   command=UpButtonClicked)


        self.UPButton.configure(
            font=tk.font.Font(family="Arial", size=30, weight="bold"),  # Bold font, ~40px adjusted to 30pt
            bg="black",               # Background color
            fg="white",               # Text color
            bd=1,                     # 1px border
            relief="solid",           # Solid border to mimic white border
            activebackground="#177bad",# Pressed state color
            activeforeground="white", # Text color when pressed
            justify="center",         # Center text horizontally
            # pady=3,
            width=3 
                                               # Vertical padding ~9px
        )
 
        

        self.DownButton = tk.Button (self.content_frame,
                                  text="-", bg="#f56c87",font=12,  
                                  width=10, command=DownButtonClicked)
    
    #load method
    def Load(self):
        steplabel = tk.Label (self.frame, text="Depth",font=Font)
        #steplabel.place (x=100, y=10)        
        self.UPButton.place (x=20,  y=40)
        DepthVal = tk.Label(self.label_frame,textvariable=str(self.depthVal),justify="center", font=Font, bg='#a0f291')
        DepthVal.place(x=70,y=90)
        self.DownButton.place (x=20,  y=140)
        self.create_side_buttons()
        
        self.content_frame.place(x=280, y=110, width=711, height=441)



        def clickFlikerButton():
            HandleFliker (ManageButton['text'])
            #globaladc.buzzer_1()
            if not self.threadCreated:
                self.worker_flik = PerodicThread.PeriodicThread(intervel,self)
                self.threadCreated=True
            if (ManageButton['text'] == Text_Fliker_OFF):
                ManageButton['text'] = Text_Fliker_ON
                flikerOn = True
                self.UPButton.config(state='active',bg='#a0f291')                
                self.DownButton.config(state='active',bg='#a0f291')           
                self.depthVal.set(7)
                if(not self.worker_flik.isStarted):
                      self.worker_flik.start()
                #else : self.resume()          
            else:
                ManageButton['text'] = Text_Fliker_OFF
                self.depthVal.set(0)
                flikerOn = False
                self.UPButton.config(state='disabled',bg='#f56c87')
                self.DownButton.config(state='disabled',bg='#f56c87')
                   
                

        ManageButton = tk.Button (self.content_frame,
                                  text=Text_Fliker_OFF,font=Font, 
                                  command=clickFlikerButton, 
                                  width=30)
        ManageButton.place (x=300,  y=300)


        def onfw():
            pageDisctonary['FlikerScreen'].hide()
            pageDisctonary['CffFovea'].show()


        def onbw():
            pageDisctonary['FlikerScreen'].hide()
            pageDisctonary['MainScreen'].show()

        fwButton = tk.Button (self.content_frame,
                                 text=">>", font=Font2,
                                 command=onfw, bg='Green',
                                 width=10)
       
        bwButton = tk.Button (self.content_frame,
                                 text="<<", font=Font2,
                                 command=onbw, bg='Green',
                                 width=10)
  

        # fwButton.place(x=620,y=500)
        # bwButton.place(x=420, y=500) 
     
        
    def create_side_buttons(self):
        """Create side navigation buttons."""
        buttons = [
            ("Flicker Demo", 150, 'white'),
            ("CFF Fovea", 210, 'black'),
            ("BRK Fovea", 270, 'black'),
            ("CFF Para-Fovea", 330, 'black'),
            ("BRK Para-Fovea", 390, 'black'),
            ("Test Result", 450, 'black')
        ]

        for text, y, bg_color in buttons:
            btn = tk.Button(self.frame, text=text, font=Font,
                          width=15, bg=bg_color,
                          fg='white' if bg_color == 'black' else 'black',
                          relief='solid', bd=2)
            btn.place(x=10, y=y)

    def hide(self):
        self.stop_therad()
        self.frame.place_forget()            
    
    def show(self):
        # globaladc.flicker_Prepair() 			# run this while loding flicller screen
        self.frame.place(width=1024,height=600)
        self.depthVal.set(0)
        flikerOn = False
        self.UPButton.config(state='disabled')
        self.DownButton.config(state='disabled')
        
    # def StopScheduler():
    #     
    def run_therad(self):
        # globaladc.get_print("worker_flik thread started")
        if not self.worker_flik.isStarted :
            self.worker_flik.start()
        else: 
            self.worker_flik.resume()       

    def stop_therad(self):
        # globaladc.get_print("worker_flik thread stopped")
        if self.threadCreated :
            self.worker_flik.stop()
            self.worker_flik.kill()
            self.threadCreated = False          
    
    def periodic_event(self):
           #fliker_dac_val = 1325+(25*self.depthVal.get())
           if self.fliker_bool == True :
                # globaladc.fliker(self.depthVal.get())#A1 GREEN_FREQ                    
                self.fliker_bool = False
                #lobaladc.get_print('event1-0')
           else:
                # globaladc.fliker(0)#A1 GREEN_FREQ  
                self.fliker_bool = True
                #lobaladc.get_print('event')   
         #this can be used to set the High/positive side of the pulse wave
    
    def getName():
        return "FlikerScreen"    
            

def main():
    root = tk.Tk()
    root.title("Flicker Control")
    root.geometry("1024x600")
    root.resizable(0, 0)

    # Create the main frame
    # main_frame = tk.Frame(root, bg="black")
    flikerFrame = tk.Frame(root, bg='black')

    # Create an instance of flikerWindow
    flicker_screen = flikerWindow(flikerFrame)
    
    # Load UI components
    flicker_screen.Load()

    # Show the flicker screen
    flicker_screen.show()

    # Start the Tkinter main loop
    root.mainloop()

if __name__ == "__main__":
    
    main()