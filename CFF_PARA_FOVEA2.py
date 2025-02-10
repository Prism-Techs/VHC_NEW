import tkinter as tk
from tkinter import  ttk       
import PerodicThread 
import time
from  BRK_FOVEA_1 import BrkFovea_1 
import PatientInfo
from globalvar import pageDisctonary
from globalvar import globaladc
import RPi.GPIO as GPIO

switch = 20

Font = ("Arial",15)
Font1 = ("Arial",15)
Font2 = ("Arial",20)
intervel = 0.21#sec
select = 1
cffValue_frq_x =820
cffValue_frq_y = 40


class CffParaFovea :
    def __init__(self, frame):
        self.frame = frame
        self.response_count = 0  
        self.skip_event =True
        self.threadCreated =False
        self.worker_cff = PerodicThread.PeriodicThread(intervel,self)
        self.freq_val_start = 35
        self.freq_val = self.freq_val_start
        self.min_apr = 0
        self.max_apr = 0 
        self.response_array = [0,0,0,0,0]
        self.trialList = tk.Listbox (frame,font=Font1,width=6)
        self.patentActionflabel = tk.Label (frame, text='Patient\'s side Button \n Begins Traial',font=Font1,bg='white')
        self.patentActionflabel_2 = tk.Label (frame, text='Increment NULL setting until\n patient reports on flicker\n Press RESUM when done',font=Font1,bg='white')
        self.cffValue_min = tk.Label (frame, text='    ', font=Font,bg='white')
        self.cffValue_max = tk.Label (frame, text='    ', font=Font,bg='white') 
        self.cffValue_frq = tk.Label (frame, text='    ', font=Font,bg='#F7F442')  
    
    def handleuserButton(self,switch):
        print('handle to be implemented')
        jmp = False
        self.patient_switch_desable()
        time.sleep(0.2)        
        if self.skip_event:
            self.patentActionflabel.place_forget()
            self.threadCreated=True
            if self.response_count != 0:
                self.freq_val_start = self.min_apr + 4.5             
            else :
                self.freq_val_start = 35
            self.freq_val=self.freq_val_start            
            self.skip_event = False             
        else :
            self.skip_event = True            
            if  self.threadCreated :
                #self.stop_therad()                                              
                self.response_array[self.response_count] = self.freq_val
                self.trialList.insert(self.response_count,self.response_array[self.response_count])
                self.response_count = self.response_count + 1                                     
                self.min_apr = globaladc.cff_min(self.min_apr,self.freq_val)                    
                self.cffValue_min.config(text = self.min_apr)
                if self.response_count == 5 :
                    self.max_apr =  globaladc.cff_max(self.response_array)                        
                    self.cffValue_max.config(text = self.max_apr)
                    print('self.max_apr=',self.max_apr)
                    self.stop_therad()                                               
                    #average the min max values and store in Guli
                    avgval = round(((self.max_apr + self.min_apr)/2),1)- 5
                    globaladc.put_cff_fovea_frq(avgval)                        
                    time.sleep(1)
                    globaladc.buzzer_3()
                    print('done')
                    pageDisctonary['CffParaFovea'].hide()
                    pageDisctonary['BrkparaFovea'].show()
                    self.patient_switch_desable()
                    jmp = True                
                self.cffValue_frq.config(text = self.freq_val)
                #globaladc.buzzer_3()
        time.sleep(0.5)
        globaladc.buzzer_3()
        if not jmp:
            self.patient_switch_enable() 
        
    def patient_switch_enable(self) :
        print('patient_switch_enable')
        GPIO.setwarnings(False) # Ignore warning for now
        GPIO.setmode(GPIO.BCM) # Use physical pin numbering
        GPIO.setup(switch, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(switch,GPIO.RISING,callback=self.handleuserButton) #CffFovea
    
    def patient_switch_desable(self) :
            print('patient_switch_desable')
            GPIO.remove_event_detect(switch) 
        
    def Load(self):
        cfflabel = tk.Label (self.frame, text='CFF PARA FOVEA :',font=Font)
        cfflabel.place (x=400, y=10)
        self.cffValue_min.place (x=430, y=40)
        self.cffValue_max.place (x=500, y=40)
        self.cffValue_frq.place (x=810, y=30)        
        self.patentActionflabel.place (x=380, y=100)
        self.trialList.place (x=800, y=60)
        
        def handleReStart():
            #userButten.place (x=375, y=440)  
            self.patentActionflabel.place(x=400,y=200)
            self.patentActionflabel_2.place_forget()
            self.reStartButton.place_forget()
            self.patient_switch_enable()
            globaladc.buzzer_3() 

#         userButten = tk.Button (self.frame,
#                                  text="userButten",
#                                  command=userButten_handle, font=Font,
#                                  width=10)
        
                    

        self.reStartButton = tk.Button (self.frame,
                                 text="RESUM",
                                 command=handleReStart, font=Font,
                                 width=10,bg='#a0f291')

        self.reStartButton.place (x=300, y=400)


        def onfw():
            pageDisctonary['CffParaFovea'].hide()
            pageDisctonary['BrkparaFovea'].show()


        def onbw():
            pageDisctonary['CffParaFovea'].hide()
            pageDisctonary['BrkFovea_1'].show()
            

        fwButton = tk.Button (self.frame,
                                 text=">>", font=Font2,
                                 command=onfw, bg='Green',
                                 width=10)
       
        bwButton = tk.Button (self.frame,
                                 text="<<", font=Font2,
                                 command=onbw, bg='Green',
                                 width=10)
  
        # fwButtn.place(x=420, y=500)
        # bwButtoon.place(x=620,y=500)
    
           
       
    def show(self):
        self.cffValue_min.config(text = '     ')
        self.cffValue_max.config(text = '     ')
        self.cffValue_frq.config(text = '     ')
        self.trialList.delete(0,tk.END)
        self.frame.place(width=1024,height=600)
        globaladc.cff_para_fovea_screen_initialize()    # run this while loding cff Fovea screen       
        self.freq_val_start = 33
        self.freq_val = self.freq_val_start
        self.cffValue_frq.config(text =self.freq_val)
        self.response_array = [0,0,0,0,0]
        self.response_count = 0 
        self.min_apr = 0
        self.max_apr = 0 
        self.skip_event = True
        self.threadCreated=False
        self.patentActionflabel.place_forget()
        self.patentActionflabel_2.place(x=380,y=200)
        self.reStartButton.place (x=400, y=350)
        self.run_therad()      
               
    
    def hide(self): 
        self.stop_therad()
        self.frame.place_forget()
        
                  

    def run_therad(self):
        print("worker_cff thread started")
        self.worker_cff = PerodicThread.PeriodicThread(intervel,self)
        if not self.worker_cff.isStarted :
            self.worker_cff.start()        
        
    def stop_therad(self):
        print("worker_cff thread stopped")
        if self.worker_cff.isStarted :
            self.worker_cff.stop()  
            self.worker_cff.kill()
            self.patient_switch_desable()
            self.skip_event = True
            self.threadCreated=False


    def periodic_event(self):
        if not self.skip_event :
            self.freq_val = round(self.freq_val - 0.2,1)
            self.cffValue_frq.config(text = self.freq_val)
            if self.freq_val == 4 :
                self.skip_event = True
                self.threadCreated=False
                self.freq_val = self.freq_val_start
                self.cffValue_frq.config(text = self.freq_val)
                globaladc.buzzer_3()                       
        else :            
            print('CP')       
        globaladc.put_cff_para_fovea_frq(self.freq_val)   

    def getName():
        return "CffPARAFovea"

#test Run class
if __name__ == '__main__':
    window = tk.Tk ()    
    CffParaFovea.Load(window)
    CffParaFovea.show()