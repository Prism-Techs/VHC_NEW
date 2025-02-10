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
switch = 20
from globalvar import CustomLabel


Font = ("Arial",15)
Font1 = ("Arial",15)
Font2 = ("Arial",20)
intervel = globaladc.get_cff_delay()  #0.208#sec
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
        self.patentActionflabel_2 = tk.Label (frame, text='Increment Patient in\n Parafoveal Viewing.\n\n Press RESUME when done',font=Font1,bg='white')
        self.cffValue_min = tk.Label (frame, text='    ', font=Font,bg='white')
        self.cffValue_max = tk.Label (frame, text='    ', font=Font,bg='white') 
        self.cffValue_frq = CustomLabel(self.content_frame, text='    ')   
        self.content_frame = tk.Frame(self.frame, bg='#1f2836')
        self.freques_frame = tk.Frame(self.content_frame,bg="black")
    
    def handleuserButton(self,switch):
        globaladc.get_print('handle to be implemented')
        jmp = False
        self.patient_switch_desable()
        time.sleep(0.2)        
        if self.skip_event:
            self.patentActionflabel.place_forget()
            self.threadCreated=True
#             if self.response_count != 0:
#                 self.freq_val_start = self.min_apr + 6.5
#             else :
#                 self.freq_val_start = 35
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
#             #globaladc.buzzer_3() 
            globaladc.fliker_start_g()
            time.sleep(0.15)
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
                self.min_apr = globaladc.get_cff_p_min_cal(self.response_count, self.freq_val)    
                self.cffValue_min.config(text = self.min_apr)           
                self.response_count = self.response_count + 1 
                if self.response_count == 5 :
                    self.max_apr =  globaladc.get_cff_p_max_cal()                     
                    self.cffValue_max.config(text = self.max_apr)
                    str_data = 'self.max_apr='+str(self.max_apr)
                    globaladc.get_print(str_data)
                    self.stop_therad()                                               
                    #average the min max values and store in Guli
                    avgval = globaladc.get_cff_p_avg_cal()
                    # globaladc.put_cff_para_fovea_frq(avgval)
                    str_data = 'self.avgval='+str(avgval)
                    globaladc.get_print(str_data)
                    log_data = "CFF_P-"+str(avgval)
                    currentPatientInfo.log_update(log_data)
                    time.sleep(1)
                    globaladc.buzzer_3()
                    globaladc.get_print('done')
                    pageDisctonary['CffParaFovea'].hide()
                    pageDisctonary['BrkparaFovea'].show()
                    self.patient_switch_desable()
                    jmp = True                
                self.cffValue_frq.config(text = self.freq_val)
                #globaladc.buzzer_3()        
        if not jmp:                        
            if self.skip_event:
                time.sleep(0.5) 
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
        self.freq_val_start = 35
        self.freq_val = self.freq_val_start
        self.min_apr = 0
        self.max_apr = 0 
        self.response_array = [0,0,0,0,0]
        self.cfflabel = tk.Label (self.frame, text='CFF PARA FOVEA :',font=Font)
        self.cfflabel.place (x=400, y=10)
        self.cffValue_min.place (x=430, y=40)
        self.cffValue_max.place (x=500, y=40)
        self.cffValue_frq.place (x=600, y=35)        
        self.patentActionflabel.place (x=380, y=100)
        self.trialList.place (x=800, y=60)
        self.content_frame.place(x=280, y=110, width=711, height=441)
        self.freques_frame.place(relx=0.3, rely=0.1, width=291, height=126)



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
                                 text="RESUME",
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
  
        # fwButton.place(x=420, y=500)
        # bwButton.place(x=620,y=500)  
       
    def show(self):
        self.cffValue_min.config(text = '     ')
        self.cffValue_max.config(text = '     ')
        self.cffValue_frq.config(text = '     ')
        self.trialList.delete(0,tk.END)
        self.frame.place(width=1024,height=600)              
        self.freq_val_start = 35
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
        self.cfflabel.place (x=400, y=10) 
        self.trialList.place (x=800, y=60)
        self.run_therad()
        self.reStartButton.place (x=300, y=400)
        globaladc.cff_Para_Fovea_Prepair()    # run this while loding cff Fovea screen 
    
    def hide(self): 
        self.stop_therad()
        self.frame.place_forget()     

    def run_therad(self):
        globaladc.get_print("worker_cff thread started")
        self.worker_cff = PerodicThread.PeriodicThread(intervel,self)
        if not self.worker_cff.isStarted :
            self.worker_cff.start()        
        
    def stop_therad(self):
        globaladc.get_print("worker_cff thread stopped")
        globaladc.main_Prepair()
        if self.worker_cff.isStarted :
            self.worker_cff.stop()  
            self.worker_cff.kill()
            self.patient_switch_desable()
            self.skip_event = True
            self.threadCreated=False

    def periodic_event(self):
        if not self.skip_event :
            self.freq_val = round((self.freq_val - 0.5),1)
            self.cffValue_frq.config(text = self.freq_val)
            if self.freq_val < 0 :
                self.skip_event = True
                self.threadCreated=False
                self.freq_val = self.freq_val_start
                self.cffValue_frq.config(text = self.freq_val)
                globaladc.buzzer_3()       
            globaladc.put_cff_para_fovea_frq(self.freq_val)                
        else :   
            globaladc.get_print('CF') 
            globaladc.put_cff_para_fovea_frq(35)            
            #globaladc.green_led_on()                          
              
          

    def getName():
        return "CffPARAFovea"

#test Run class
if __name__ == '__main__':
    window = tk.Tk ()    
    CffParaFovea.Load(window)
    CffParaFovea.show()