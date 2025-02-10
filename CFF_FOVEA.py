import tkinter as tk
from tkinter import  ttk       
import PerodicThread 
import time
from  BRK_FOVEA_1 import BrkFovea_1 
import PatientInfo
from globalvar import pageDisctonary
from globalvar import globaladc
import RPi.GPIO as GPIO
from globalvar import currentPatientInfo
from tkinter import font
from header import HeaderComponent


switch = 20
contt_fva = 34.5
Font = ("Arial",15)
Font1 = ("Arial",15)
Font2 = ("Arial",20)
intervel = globaladc.get_cff_delay()
select = 1
cffValue_frq_x =820
cffValue_frq_y = 40




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
        self.place(x=700, y=30)



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







def hardware():
        CffFovea.handleuserButton()

class CffFovea :
    def __init__(self, frame):
        self.frame = frame
        self.frame.config(bg='black')
        self.response_count = 0  
        self.skip_event =True
        self.threadCreated =False
        self.worker_cff = PerodicThread.PeriodicThread(intervel,self)
        self.freq_val_start = 34.5
        self.freq_val = self.freq_val_start
        self.min_apr = 0
        self.max_apr = 0 
        self.response_array = [0,0,0,0,0]
        self.trialList = tk.Listbox (frame,font=Font1,width=6)
        self.patentActionflabel = tk.Label (frame, text='Patient\'s side Button \n Begins Traial',font=Font1,bg='white')
        self.cffValue_min = tk.Label (frame, text='    ', font=Font,bg='white')
        self.cffValue_max = tk.Label (frame, text='    ', font=Font,bg='white') 
        self.cffValue_frq = tk.Label (frame, text='    ', font=Font,bg='#F7F442')  
    
    def handleuserButton(self,switch):
        globaladc.get_print('handle to be implemented')
        jmp = False
        self.patient_switch_desable()
        time.sleep(0.15)        
        if self.skip_event:
            self.patentActionflabel.place_forget()
            self.threadCreated=True
            if self.response_count == 0:
                self.freq_val_start = self.freq_val_start
            elif self.response_count == 1:
                self.freq_val_start = self.min_apr + 6.5
            elif self.response_count == 2:
                self.freq_val_start = self.min_apr + 6.5
            elif self.response_count == 3:
                self.freq_val_start = self.min_apr + 6.5
            elif self.response_count == 4:
                self.freq_val_start = self.min_apr + 6.5
            elif self.response_count == 5:
                self.freq_val_start = self.min_apr + 6.5
            else :
                self.freq_val_start = self.min_apr + 6.5
            self.freq_val=self.freq_val_start   
            #globaladc.buzzer_1() 
            globaladc.fliker_start_g()
            time.sleep(0.2)             
            self.skip_event = False            
        else :
            self.skip_event = True
            time.sleep(0.5) 
            #globaladc.buzzer_1()  
            #globaladc.green_led_on()      
           
            if  self.threadCreated :
                #self.stop_therad()                                              
                self.response_array[self.response_count] = self.freq_val
                self.trialList.insert(self.response_count,self.response_array[self.response_count])                
                self.min_apr = globaladc.get_cff_f_min_cal(self.response_count, self.freq_val)  
                self.response_count = self.response_count + 1
                #self.min_apr = globaladc.cff_min(self.min_apr,self.freq_val)                    
                self.cffValue_min.config(text = self.min_apr)                
                if self.response_count == 5 :
                    self.max_apr =  globaladc.get_cff_f_max_cal()                        
                    self.cffValue_max.config(text = self.max_apr)                    
                    str_data = 'self.max_apr=' + str(self.max_apr)
                    globaladc.get_print(str_data)            
                    self.stop_therad()                                               
                    #average the min max values and store in Guli
                    avgval = globaladc.get_cff_f_avg_cal()
                    # globaladc.put_cff_fovea_frq(avgval)
                    log_data = "CFF_F-"+str(avgval)
                    currentPatientInfo.log_update(log_data)                    
                    time.sleep(1)
                    globaladc.buzzer_3()
                    globaladc.get_print('done')
                    pageDisctonary['CffFovea'].hide()
                    pageDisctonary['BrkFovea_1'].show()
                    self.patient_switch_desable()
                    jmp = True                
                self.cffValue_frq.config(text = self.freq_val)  
        if not jmp:
            if self.skip_event:
                time.sleep(0.2) 
                globaladc.buzzer_3()            
            self.patient_switch_enable() 
           
    def patient_switch_enable(self) :
        globaladc.get_print('patient_switch_enable')
        GPIO.setwarnings(False) # Ignore warning for now
        GPIO.setmode(GPIO.BCM) # Use physical pin numbering
        GPIO.setup(switch, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(switch,GPIO.RISING,callback=self.handleuserButton) #CffFovea
                
    def patient_switch_desable(self) :
            globaladc.get_print('patient_switch_desable')
            GPIO.remove_event_detect(switch)
   
    def Load(self):
        self.response_count = 0  
        self.skip_event =True
        self.threadCreated =False
        self.worker_cff = PerodicThread.PeriodicThread(intervel,self)
        self.freq_val_start = 34.5
        self.freq_val = self.freq_val_start
        self.min_apr = 0
        self.max_apr = 0 
        self.response_array = [0,0,0,0,0]
        cfflabel = tk.Label (self.frame, text='CFF FOVEA :',font=Font)
        cfflabel.place (x=420, y=10)
        self.cffValue_min.place (x=430, y=40)
        self.cffValue_max.place (x=500, y=40)
        self.cffValue_frq.place (x=810, y=30)        
        self.patentActionflabel.place (x=380, y=100)
        self.trialList.place (x=800, y=60)
        
        
        #         userButton = tk.Button (self.frame,
#                                  text="User",
#                                  command=handleuserButton, font=Font,
#                                  width=10)

# 
#         userButton.place (x=100, y=300) 

        def onfw():
            pageDisctonary['CffFovea'].hide()
            pageDisctonary['MainScreen'].show()

        def onbw():
            pageDisctonary['CffFovea'].hide()
            pageDisctonary['BrkparaFovea'].show()
        #pageDisctonary['MainScreen'].show()

        fwButton = tk.Button (self.frame,
                                    text=">>", font=Font2,
                                    command=onfw, bg='Green',
                                    width=10)
        
        bwButton = tk.Button (self.frame,
                                    text="<<", font=Font2,
                                    command=onbw, bg='Green',
                                    width=10)

        # fwButton.place(x=620,y=500)
        # bwButton.place(x=420, y=500)    

    def show(self):
        self.cffValue_min.config(text = '     ')
        self.cffValue_max.config(text = '     ')
        self.cffValue_frq.config(text = '     ')
        self.trialList.delete(0,tk.END)
        self.frame.place(width=1024,height=600)
        self.patentActionflabel.place (x=380, y=100)
        globaladc.cff_Fovea_Prepair() # run this while loding cff Fovea screen        
        self.freq_val_start = 34.5
        self.freq_val = self.freq_val_start
        self.response_array = [0,0,0,0,0]
        self.response_count = 0 
        self.min_apr = 0
        self.max_apr = 0 
        self.skip_event = True
        self.threadCreated=False
        self.run_therad() 
        globaladc.blue_led_off()   
    
    def hide(self): 
        self.stop_therad()
        self.frame.place_forget()
        
    def run_therad(self):
        globaladc.get_print("worker_cff thread started")        
        self.worker_cff = PerodicThread.PeriodicThread(intervel,self)
        if not self.worker_cff.isStarted :
            self.worker_cff.start()
            self.patient_switch_enable()
        
    def stop_therad(self):
        globaladc.get_print("worker_cff thread stopped")
        if self.worker_cff.isStarted :
            self.worker_cff.stop()  
            self.worker_cff.kill()
            self.patient_switch_desable()
            self.skip_event = True
            self.threadCreated=False

    def print_min(self):
        globaladc.get_print('from dac CffFovea.min_apr = ',self.min_apr)

    def periodic_event(self):
        if not self.skip_event :
            self.freq_val = round((self.freq_val - 0.5),1)
            self.cffValue_frq.config(text = self.freq_val)
            if self.freq_val <  5 :
                self.skip_event = True
                self.threadCreated=False
                self.freq_val = self.freq_val_start
                self.cffValue_frq.config(text = self.freq_val)
                globaladc.buzzer_3()
            globaladc.put_cff_fovea_frq(self.freq_val)
        else :
            globaladc.put_cff_fovea_frq(35)
            globaladc.get_print('CF') 
            #globaladc.green_led_on()            
            
            
    def getName():
        return "CffFovea"

#test Run class
if __name__ == '__main__':
    window = tk.Tk ()    
    CffFovea.Load(window)
    CffFovea.show()