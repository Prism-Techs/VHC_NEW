import imp
import tkinter as tk
from tkinter import  IntVar, ttk       
from globalvar import pageDisctonary
from globalvar import globaladc
from globalvar import currentPatientInfo
import PerodicThread
import RPi.GPIO as GPIO
import time
from header import HeaderComponent

switch = 20
Font = ("Arial",15)
Font1 = ("Arial",15)
Font2 = ("Arial",20)

defaultdepth = 11
maxdepth_1 = 225
maxdepth_2 = 2.00
intervel = globaladc.get_brk_delay()   #0.128
resume_spot_x = 450
resume_spot_y = 240

class BrkparaFovea :
    def __init__(self, frame):        
        self.worker_brk_f = PerodicThread.PeriodicThread(intervel,self)
        self.value = 0
        self.locate = 0
        self.inc_dec_2 = False
        self.skip_event =True
        self.threadCreated =False
        self.pre_brk_mid = 11     
        self.frame = frame
        self.frame.config(bg='black')
        self.content_frame = tk.Frame(frame, bg='#1f2836')
        self.trialList_min = tk.Listbox (self.content_frame,font=Font1,width=5, bg='black',fg='red',justify='center')
        self.trialList_mid = tk.Listbox (self.content_frame,font=Font1,width=5, bg='black',fg='red',justify='center')
        self.trialList_max = tk.Listbox (self.content_frame,font=Font1,width=5, bg='black',fg='red',justify='center')
        self.depthVal = tk.IntVar()
        self.brk_min = tk.IntVar()
        self.brk_max = tk.IntVar()
        self.depthVal_2 = tk.DoubleVar()        
        self.depthVal.set(defaultdepth)  
        self.threadCreated =False
        self.save_enable_text = tk.Label (frame,font=Font1,bg='white')
        self.process = 0 

        def UpButtonClicked():
            globaladc.buzzer_1()
            if self.process == 0 :                
                if(self.depthVal.get() < maxdepth_1):
                    x = self.depthVal.get()+10
                    if (x >= 225) :
                        x = 225
                    self.depthVal.set(x)
                    self.value = x
                    self.pre_brk_mid = x
                    globaladc.blue_led_Freq_control(x)
                    self.trialList_mid.delete(self.locate) 
                    self.trialList_mid.insert(self.locate,x) 
            elif self.process == 1 :
                cff_fovea_frq = globaladc.get_cff_para_fovea_frq()
                if(self.depthVal_2.get() < maxdepth_2):
                    x = round((self.depthVal_2.get()+0.5)+0.00555555,1)
                    str_data = 'x='+str(x)
                    globaladc.get_print(str_data)
                    self.depthVal_2.set(x)                    
                    globaladc.put_cff_para_fovea_frq(round((cff_fovea_frq+0.5)+0.00555555,1))


        self.UPButton =tk.Button(self.content_frame, text="+",
                                 font=('Helvetica', 30, 'bold'),
                                 width=2, height=1,
                                 bg='black', fg='white',
                                 command=UpButtonClicked,
                                 relief='solid', borderwidth=1)


        def DownButtonClicked():
            globaladc.buzzer_1()
            if self.process == 0 :                
                if (self.depthVal.get() > 0): 
                    x =self.depthVal.get()-10
                    if (x <= 11) :
                        x = 11
                    self.depthVal.set(x)
                    self.value = x
                    self.pre_brk_mid = x
                    globaladc.blue_led_Freq_control(x)
                    self.trialList_mid.delete(self.locate) 
                    self.trialList_mid.insert(self.locate,x) 
            elif self.process == 1 :
                cff_fovea_frq = globaladc.get_cff_para_fovea_frq()
                y = self.depthVal_2.get()
                if(y > 0):
                    x = round((y-0.5)+0.00555555,1)
                    self.depthVal_2.set(x)
                    globaladc.put_cff_para_fovea_frq(round((cff_fovea_frq-0.5)+0.00555555,1))            
                   
        self.DownButton = tk.Button(self.content_frame, text="-",
                                   font=('Helvetica', 30, 'bold'),
                                   width=2, height=1,
                                   bg='black', fg='white',
                                   command=DownButtonClicked,
                                   relief='solid', borderwidth=1)   
#         def non ():
#             globaladc.get_print('non')
            
#         def handleSave():
#             globaladc.get_print('Save handle to be implemented')
#             self.saveButton.config(command=non,text="Busey",bg='#f24e79')
#             currentPatientInfo.Save_brk_p()
#             #onfw():
#             pageDisctonary['BrkparaFovea'].hide()
#             pageDisctonary['MainScreen'].show()
#             self.patient_switch_desable()
            
            # with open('textfile.txt','a') as s:
            #   for i in range(self.listView.model().rowCount()):
            #    text = self.listView.item(i).text()
            # # globaladc.get_print(i, text)
            # s.write(text)   
        
    def handleuserButton(self,switch):
            self.patient_switch_desable()            
            time.sleep(0.2)
            jmp = False
            globaladc.get_print('to be implemented')            
            if not self.process_chainge:                
                if not self.skip_event :
                    self.skip_event = True 
                    #globaladc.buzzer_1() 
                    self.locate = 0
                    if not self.rptloop :                        
                        if self.inc_dec_1 :
                            self.inc_dec_1 = False                            
                        else :
                            self.inc_dec_1 = True 
                        if self.inc_dec_2 :
                            self.process_chainge = True                            
                            brk_min = int(self.trialList_min.get(self.locate))
                            brk_max = int(self.trialList_max.get(self.locate))
                            brk_mid = globaladc.get_brk_para_f_mid_calc(self.locate, brk_min, brk_max)
                            str_data = 'l='+str(brk_min)+',m='+str(brk_mid)+',r='+str(brk_max)
                            globaladc.get_print(str_data)

                            self.trialList_mid.delete(self.locate)
                            self.trialList_mid.insert(self.locate,brk_mid)
                            
                            if abs(self.pre_brk_mid - brk_mid)>5:
                                self.pre_brk_mid = brk_mid
                                self.process_chainge = False
                                
                            if self.process_chainge :   
                                self.patentActionflabel_3.place_forget()
                                self.DownButton.place_forget()
                                self.UPButton.place_forget()
                                self.null_box.place_forget()
                                self.DepthVal.place_forget()
                                self.inc_dec_1 = True   #extra add 
                            
                            # globaladc.brk_para_fovea_3_screen_initialize()                             
                            leng = self.trialList_max.size()
                            self.trialList_max.delete(0,leng-1)
                            leng = self.trialList_min.size()
                            self.trialList_min.delete(0,leng-1)
                            leng = self.trialList_mid.size()
                            #globaladc.buzzer_3()
                            self.inc_dec_2 = False
                            self.value = self.trialList_mid.get(self.locate)
                else :                    
                    self.value = self.trialList_mid.get(self.locate)
                    #globaladc.buzzer_3()
                    self.skip_event = False                    
                    self.patentActionflabel_2.place_forget()
                    self.rptloop = False
            else : 
                if not self.skip_event :
                    self.skip_event = True
                    #globaladc.buzzer_1()
                    if not self.rptloop :                            
                        if self.inc_dec_1 :
                            self.inc_dec_1 = False
                        else :
                            self.inc_dec_1 = True
                        if not self.inc_dec_2 :
                            brk_min = int(self.trialList_min.get(self.locate))
                            brk_max = int(self.trialList_max.get(self.locate))
                            brk_mid = globaladc.get_brk_para_f_mid_calc(self.locate + 1, brk_min, brk_max)
                            str_data = 'l='+ str(brk_min)+',m='+ str(brk_mid)+',r='+str(brk_max)
                            globaladc.get_print(str_data)                        
                            self.locate = self.locate + 1
                            self.trialList_mid.insert(self.locate,brk_mid) 

                        if self.locate == 4 :                            
                            #self.userButton.place_forget()
                            # globaladc.put_brk_para_fovea_frq(self.trialList_mid.get(self.locate))
                            cff_p = globaladc.get_cff_p_max_cal()                            
#                             get_f_sd=globaladc.get_f_sd()
                            cff_s = globaladc.get_cff_p_avg_cal()
                            globaladc.put_cff_fovea_frq(cff_s) #cff

                            log_data = "cff_p_min-["+str(globaladc.get_cff_p_min_all())+"]"
                            currentPatientInfo.log_update(log_data)                            
                            log_data = "cff_p_max-["+str(globaladc.get_cff_p_max_all())+"]"
                            currentPatientInfo.log_update(log_data)
                            log_data = "cff_p_avg-["+str(globaladc.get_cff_p_avg_all())+"]"
                            currentPatientInfo.log_update(log_data)
                            
                            log_data = "Bfp_min-["+str(globaladc.get_brk_para_f_min_all())+"]"
                            currentPatientInfo.log_update(log_data)
                            log_data = "Bfp_mid-["+str(globaladc.get_brk_para_f_mid_all())+"]"
                            currentPatientInfo.log_update(log_data)
                            log_data = "Bfp_max-["+str(globaladc.get_brk_para_f_max_all())+"]"
                            currentPatientInfo.log_update(log_data)
                                                        
                            time.sleep(0.5)
                            get_f_mpod =globaladc.get_cal_f_mpod() 
                            f_sd_val = globaladc.get_cal_f_sd()                           
                            currentPatientInfo.SetCFF_F(cff_s)
                            currentPatientInfo.SetCFF_P(cff_p) #f_sd                            
                            currentPatientInfo.SetF_mpod(get_f_mpod)
                            currentPatientInfo.SetF_SD(f_sd_val)
                            globaladc.put_save_no(2)
                            # home run
                            self.patient_switch_desable()
                            log_data = "F_SD-"+str(f_sd_val)
                            currentPatientInfo.log_update(log_data)
                            globaladc.all_led_off()
                            time.sleep(2)
                            globaladc.get_print('call save butten to save MPOD')
                            jmp = True
                            self.saveButton.place (x=100, y=340)
                            #globaladc.buzzer_3()
                else :                    
                    self.value = self.trialList_mid.get(self.locate)
                    #globaladc.buzzer_1()
                    self.skip_event = False                    
                    self.patentActionflabel_2.place_forget()
                    self.rptloop = False  
            self.value = self.trialList_mid.get(self.locate)            
            if not jmp:                
                self.patient_switch_enable()            
                if self.skip_event:
                    time.sleep(0.5) 
                    globaladc.buzzer_3()
               
        
        
    def patient_switch_enable(self) :
        globaladc.get_print('patient_switch_enable')
        GPIO.setwarnings(False) # Ignore warning for now
        GPIO.setmode(GPIO.BCM) # Use physical pin numbering
        GPIO.setup(switch, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(switch,GPIO.RISING,callback=self.handleuserButton) #CffFovea
    
    def patient_switch_desable(self) :
        globaladc.get_print('patient_switch_desable')
        GPIO.remove_event_detect(switch)      
        
    def create_side_buttons(self):
        """Create side navigation buttons."""
        buttons = [
            ("Flicker Demo", 150, 'black'),
            ("CFF Fovea", 210, 'black'),
            ("BRK Fovea", 270, 'black'),
            ("CFF Para-Fovea", 330, 'black'),
            ("BRK Para-Fovea", 390, 'white'),
            ("Test Result", 450, 'black')
        ]

        for text, y, bg_color in buttons:
            btn = tk.Button(self.frame, text=text, font=Font,
                          width=20, bg=bg_color,
                          fg='white' if bg_color == 'black' else 'black',
                          relief='solid', bd=2)
            btn.place(x=10, y=y)

        
        
    def Load(self):
        self.patentActionflabel = tk.Label (self.frame, text='Increment Null Setting untill \nPatient Reports no fliker,\nPress resume when done',font=Font1,bg='white')
        self.patentActionflabel_3 = tk.Label (self.frame, text='IF Require\nVary NULL settings until\npatient reports on flicker',font=Font1,bg='white')
        self.brk_parf_label = tk.Label(self.content_frame,text='BRK PARA FOVEA',bg="yellow", font= Font, width=18)  
        self.null_box = tk.Label(self.content_frame,text='NULL',bg="white", font= Font, width=12)      
        self.content_frame.place(x=280, y=110, width=711, height=441)

        self.patentActionflabel_2 = tk.Label (self.frame, text='Patient\'s side Button \n Begins Traial',font=Font1,bg='white')
        self.trialList_min.place (x=750, y=40)
        self.trialList_min.place (x=450, y=60)
        self.brk_parf_label.place (x=500,y=10)
        self.trialList_mid.place (x=520, y=60)
        self.trialList_max.place (x=590, y=60)
        self.patentActionflabel.place(x=350, y=20)    
        self.trialList_mid.insert(0,160)
        self.create_side_buttons()
        

        self.header = HeaderComponent(
            self.frame,
            "Macular Densitometer                                                          BRK-Para Fovea Test"
        )
        


        self.inc_dec_1 = False 
        self.inc_dec_2 = False  
        self.process_chainge = True       

        self.DepthVal = tk.Label(self.content_frame, text="15",
                                   font=('Helvetica Rounded', 28, 'bold'),
                                   width=3, height=1,
                                   bg='#1f2836', fg='white',
                                   textvariable=str(self.depthVal))
        self.DepthVal.place(x=100,y=130)
        self.UPButton.place (x=110,  y=75)   
        self.DownButton.place (x=110,  y=200)
        self.saveButton.place_forget()
        #saveButton.place (x=100, y=340)
      
        #self.saveButton['state'] = tk.enable

        def handleResume():
            globaladc.buzzer_3()
            globaladc.get_print('to be implemented')
            # globaladc.brk_para_fovea_2_screen_initialize() 
            self.DepthVal.config(textvariable=str(self.depthVal_2))
            self.process = 1
            self.process_chainge = False
            self.resumeButton.place_forget()
            self.patentActionflabel.place_forget()
            self.patentActionflabel_3.place(x=350, y=20)
            self.patentActionflabel_2.place (x=375, y=120)
            #self.userButton.place (x=375, y=440)  
            self.patient_switch_enable()

        self.resumeButton = tk.Button(self.content_frame,
                                 text="Resume",
                                 command=handleResume, font=Font, bg='Orange',
                                 width=10)

        self.resumeButton.place(x=resume_spot_x,y=resume_spot_y)


#         self.userButton = tk.Button(self.frame,
#                                  text="USER",
#                                  command=handleuser, font=Font, bg='Orange',
#                                  width=10)

        def onfw():
            pageDisctonary['BrkparaFovea'].hide()
            pageDisctonary['MainScreen'].show()
            globaladc.get_print("no fw screen")

        def onbw():
            pageDisctonary['BrkparaFovea'].hide()
            pageDisctonary['MainScreen'].show()

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
        self.frame.place(width=1024,height=600)
        # globaladc.brk_para_fovea_1_screen_initialize()           # run this while loding brk fovea 1st screen
        self.skip_event = True
        self.threadCreated=False
        self.run_therad()        
        self.process = 0
        self.value = defaultdepth
        self.locate = 0
        self.pre_brk_mid = 11
        self.inc_dec_2 = False
        self.skip_event =True
        self.threadCreated =False
        leng = self.trialList_max.size()
        self.trialList_max.delete(0,leng-1)
        leng = self.trialList_min.size()
        self.trialList_min.delete(0,leng-1)
        leng = self.trialList_mid.size()
        self.trialList_mid.delete(0,leng-1)
        self.trialList_mid.insert(0,defaultdepth)
        self.DepthVal.config(textvariable=str(self.depthVal))
        self.DepthVal.place(x=100,y=130)
        self.resumeButton.place(x=resume_spot_x,y=resume_spot_y)
        #self.userButton.place_forget()
        self.patient_switch_desable()
        self.patentActionflabel.place(x=350, y=20)
        self.patentActionflabel_3.place_forget()
        self.patentActionflabel_2.place_forget ()
        self.UPButton.place(x=110, y=75)   
        self.DownButton.place(x=110, y=200)
        self.inc_dec_1 = False
        self.null_box.place (x=100,y=20)
        globaladc.brk_Para_Fovea_Prepair()
  
    def hide(self):
        self.stop_therad()
        self.frame.place_forget()
        
        
    
    def setRunTestScreen(self, runtestScreen):
        self.runtestScreen = runtestScreen

    def run_therad(self):
        globaladc.get_print("worker_brk_f thread started")
        self.worker_brk_f = PerodicThread.PeriodicThread(intervel,self)
        if not self.worker_brk_f.isStarted :
            self.worker_brk_f.start()  
            self.threadCreated=True         
        
    def stop_therad(self):
        globaladc.get_print("worker_brk_f thread stopped")
        if self.worker_brk_f.isStarted :
            self.worker_brk_f.stop()  
            self.worker_brk_f.kill()
            self.skip_event = True
            self.threadCreated=False

    def periodic_event(self):
        if not self.skip_event :
            if self.inc_dec_1 :
                if self.value == 250 :
                    self.trialList_max.delete(self.locate) 
                    self.rptloop = True
                    globaladc.buzzer_3()                    
                    self.skip_event = True
                else :                    
                    self.inc_dec_2 = True                 
                    self.value = self.value + 1
                    self.trialList_max.delete(self.locate)                
                    self.trialList_max.insert(self.locate,self.value)                    
            else :
                if self.value == 0 :
                    self.trialList_min.delete(self.locate) 
                    self.rptloop = True                    
                    self.trialList_min.delete(self.locate)
                    globaladc.buzzer_3()
                    self.skip_event = True                   
                else : 
                    self.inc_dec_2 = False 
                    self.value = self.value - 1
                    self.trialList_min.delete(self.locate) 
                    self.trialList_min.insert(self.locate,self.value)                
        else :            
            globaladc.get_print('BFP')
        globaladc.blue_led_Freq_control(self.value)


    def getName():
        return "BrkparaFovea"    