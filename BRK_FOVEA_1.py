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

defaultdepth = 1
maxdepth_1 = 19
maxdepth_2 = 2.00
resume_spot_x = 450
resume_spot_y = 240

class BrkFovea_1 :
    def __init__(self, frame):  
        self.intervel=globaladc.get_brk_delay()    #0.128             
        self.worker_brk_f = PerodicThread.PeriodicThread(self.intervel,self)
        self.value = 0
        self.locate = 0
        self.pre_brk_mid = 160
        self.inc_dec_2 = False
        self.skip_event =True
        self.threadCreated =False        

        def depthincrement_callback():
           # self.trialList_mid.listvariable =  self.depth_increment.get(1)
           globaladc.get_print('increment call back') 

        self.frame = frame
        self.frame.configure(background='black')
        self.content_frame = tk.Frame(frame, bg='#1f2836')
        self.trialList_min = tk.Listbox (self.content_frame,font=Font1,width=5, bg='black',fg='red',justify='center')
        self.trialList_mid = tk.Listbox (self.content_frame,font=Font1,width=5, bg='black',fg='red',justify='center')
        self.trialList_max = tk.Listbox (self.content_frame,font=Font1,width=5, bg='black',fg='red',justify='center')
        self.frame = frame
        self.depthVal = tk.IntVar()
        self.brk_min = tk.IntVar()
        self.brk_max = tk.IntVar()
        self.depthVal_2 = tk.DoubleVar()        
        self.depthVal.set(defaultdepth)  
        self.threadCreated =False
        self.save_enable_text = tk.Label (self.content_frame,font=Font1,bg='white')
        self.process = 0 
            # with open('textfile.txt','a') as s:
            #   for i in range(self.listView.model().rowCount()):
            #    text = self.listView.item(i).text()
            # # globaladc.get_print(i, text)
            # s.write(text) 
            
        def UpButtonClicked():
            globaladc.buzzer_1()
            if self.process == 0 :
                y = self.depthVal.get()
                if(y < maxdepth_1):
                    x = y+1
                    self.depthVal.set(x)
                    globaladc.blue_led_volt_control(0,x)
                    log_data = "B_V_null-["+str(x)+"]"
                    currentPatientInfo.log_update(log_data) 
                if self.depthVal.get() == 19:
                    self.save_enable_text.config(text='MPOD 1.0+\nSelect SAVE')
                    self.save_enable_text.place (x=100, y=300)
                    self.saveButton.place (x=100, y=380)
                    self.resumeButton.place_forget()
                else :
                    self.save_enable_text.place_forget()
                    self.saveButton.place_forget()
                    self.resumeButton.place(x=resume_spot_x,y=resume_spot_y)
            elif self.process == 1 :
                cff_fovea_frq = globaladc.get_cff_fovea_frq()
                if(self.depthVal_2.get() < maxdepth_2):    #self.depthVal_2.get()
                    #x = round((self.depthVal_2.get()+0.5)+0.00555555,1) #depthVal_2
                    x = round((self.depthVal_2.get()+0.5),1) #depthVal_2
                    str_data = 'x='+str(x)                       
                    globaladc.get_print(str_data)
                    self.depthVal_2.set(x)                    
                    globaladc.put_cff_fovea_frq(round((cff_fovea_frq+0.5)+0.00555555,1))


        self.UPButton =tk.Button(self.content_frame, text="+",
                                 font=('Helvetica', 30, 'bold'),
                                 width=2, height=1,
                                 bg='black', fg='white',
                                 command=UpButtonClicked,
                                 relief='solid', borderwidth=1)

        def DownButtonClicked():
            globaladc.buzzer_1()
            if self.process == 0 :
                if(self.depthVal.get() > 0):
                    x= self.depthVal.get()-1
                    self.depthVal.set(x)
                    globaladc.blue_led_volt_control(0,x)
                    log_data = "B_V_null-["+str(x)+"]"
                    currentPatientInfo.log_update(log_data)
                if self.depthVal.get() == 0:
                    self.save_enable_text.config(text='NEGLIGIBLE MPOD\nSelect SAVE')
                    self.save_enable_text.place (x=80, y=300)
                    self.saveButton.place (x=100, y=380)
                    self.resumeButton.place_forget()
                else :
                    self.save_enable_text.place_forget()
                    self.saveButton.place_forget()
                    self.resumeButton.place(x=resume_spot_x,y=resume_spot_y)
            elif self.process == 1 :
                cff_fovea_frq = globaladc.get_cff_fovea_frq()
                y = self.depthVal_2.get()
                if(y > 0):
                    x = round((y-0.5)+0.00555555,1)
                    self.depthVal_2.set(x)
                    globaladc.put_cff_fovea_frq(round((cff_fovea_frq-0.5)+0.00555555,1))
                    
        self.DownButton = tk.Button(self.content_frame, text="-",
                                   font=('Helvetica', 30, 'bold'),
                                   width=2, height=1,
                                   bg='black', fg='white',
                                   command=DownButtonClicked,
                                   relief='solid', borderwidth=1)   



    def create_side_buttons(self):
        """Create side navigation buttons."""
        buttons = [
            ("Flicker Demo", 150, 'black'),
            ("CFF Fovea", 210, 'black'),
            ("BRK Fovea", 270, 'white'),
            ("CFF Para-Fovea", 330, 'black'),
            ("BRK Para-Fovea", 390, 'black'),
            ("Test Result", 450, 'black')
        ]

        for text, y, bg_color in buttons:
            btn = tk.Button(self.frame, text=text, font=Font,
                          width=20, bg=bg_color,
                          fg='white' if bg_color == 'black' else 'black',
                          relief='solid', bd=2)
            btn.place(x=10, y=y)


    def handleuser(self,switch):
        #globaladc.get_print('to be implemented')
        self.patient_switch_desable()
        time.sleep(0.2)
        jmp = False
        if self.process_chainge < 1:### Check------------------ 2 to 1
            mod_ch = True
            if not self.skip_event :
                self.skip_event = True
                time.sleep(0.2)                
                self.locate = 0
                if not self.rptloop :                        
                    if self.inc_dec_1 :
                        self.inc_dec_1 = False                            
                    else :
                        self.inc_dec_1 = True  
                    if self.inc_dec_2 :
                        self.process_chainge = self.process_chainge + 1                            
                        brk_min = int(self.trialList_min.get(self.locate))
                        brk_max = int(self.trialList_max.get(self.locate))
                        brk_mid = globaladc.get_brk_fovea_mid_calc(self.locate, brk_min, brk_max)
                        str_data = 'l='+str(brk_min)+',m='+str(brk_mid)+',r='+str(brk_max)
                        globaladc.get_print(str_data)                        
                        self.trialList_mid.delete(self.locate)
                        self.trialList_mid.insert(self.locate,brk_mid)
                        
                        if abs(self.pre_brk_mid - brk_mid)>15:
                            self.process_chainge = 0
                            self.pre_brk_mid = brk_mid                            
                            
                        if self.process_chainge == 1:
                            self.patentActionflabel_3.place_forget()
                            self.DownButton.place_forget()
                            self.UPButton.place_forget()
                            self.null_box.place_forget()
                            self.DepthVal.place_forget()
                            # globaladc.brk_fovea_3_screen_initialize()                             
                            leng = self.trialList_max.size()
                            self.trialList_max.delete(0,leng-1)
                            leng = self.trialList_min.size()
                            self.trialList_min.delete(0,leng-1)                            
                            self.inc_dec_1 = True   #extra add 
                            #globaladc.buzzer_3()
                        self.inc_dec_2 = False                             
            else : 
                self.skip_event = False
                self.patentActionflabel_2.place_forget()
                self.rptloop = False
        else :
#             if mod_ch:
#                 globaladc.buzzer_3()
#                 mod_ch = False
            if not self.skip_event :
                self.skip_event = True
                time.sleep(0.2)
#                 globaladc.buzzer_3()
                if not self.rptloop :                 #----False, true inter chainge           
                    if not self.inc_dec_1 :
                        self.inc_dec_1 = True
                    else :
                        self.inc_dec_1 = False                            
                    if  not self.inc_dec_2 :
                        brk_min = int(self.trialList_min.get(self.locate))
                        brk_max = int(self.trialList_max.get(self.locate))
                        brk_mid = globaladc.get_brk_fovea_mid_calc(self.locate + 1, brk_min, brk_max)
                        str_data = 'l='+ str(brk_min)+',m='+ str(brk_mid)+',r='+str(brk_max)
                        globaladc.get_print(str_data)                        
                        self.locate = self.locate + 1
                        self.trialList_mid.insert(self.locate,brk_mid)    
                    if self.locate == 4 :                            
                        #self.userButton.place_forget()
                        f_val = globaladc.get_cff_fovea_frq()
                        currentPatientInfo.SetCFF_F(f_val)
                        # globaladc.put_brk_fovea_frq(self.trialList_mid.get(self.locate))
                        # f_mpod=globaladc.get_cal_f_mpod(int(self.trialList_mid.get(0)),int(self.trialList_mid.get(1)),int(self.trialList_mid.get(2)),int(self.trialList_mid.get(3)),int(self.trialList_mid.get(4)))
                        # currentPatientInfo.SetF_mpod(f_mpod)
                        globaladc.put_save_no(1) 
                        globaladc.all_led_off()

                        log_data = "cff_f_min-["+str(globaladc.get_cff_f_min_all())+"]"
                        currentPatientInfo.log_update(log_data)
                        log_data = "cff_f_max-["+str(globaladc.get_cff_f_max_all())+"]"
                        currentPatientInfo.log_update(log_data)
                        log_data = "cff_f_avg-["+str(globaladc.get_cff_f_avg_all())+"]"
                        currentPatientInfo.log_update(log_data)

                        log_data = "Bf_min-["+str(globaladc.get_brk_fovea_min_all())+"]"
                        currentPatientInfo.log_update(log_data)
                        log_data = "Bf_mid-["+str(globaladc.get_brk_fovea_mid_all())+"]"
                        currentPatientInfo.log_update(log_data)
                        log_data = "Bf_max-["+str(globaladc.get_brk_fovea_max_all())+"]"
                        currentPatientInfo.log_update(log_data)
                        time.sleep(0.5)      
                        # home run                      
                        # globaladc.get_print('call save butten to save MPOD')
                        # globaladc.get_print('jump to cff para fovea')
                        pageDisctonary['BrkFovea_1'].hide()
                        pageDisctonary['CffParaFovea'].show()
                        # globaladc.put_brk_fovea_frq(self.trialList_mid.get(self.locate + 1))
                        jmp = True
                        globaladc.buzzer_3()                        
                        self.patient_switch_desable()
            else : 
                #globaladc.buzzer_1()
                self.skip_event = False
                self.patentActionflabel_2.place_forget()
                self.rptloop = False  
        self.value = self.trialList_mid.get(self.locate)
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
        GPIO.add_event_detect(switch,GPIO.RISING,callback=self.handleuser) #CffFovea

    def patient_switch_desable(self) :
        globaladc.get_print('patient_switch_desable')
        GPIO.remove_event_detect(switch)
    
    def handleResume(self):
        globaladc.buzzer_3()
        globaladc.get_print('to be implemented')
        # globaladc.brk_fovea_2_screen_initialize() 
        self.DepthVal.config(textvariable=str(self.depthVal_2))
        self.process = 1
        self.pre_brk_mid = 160
        self.process_chainge = 0
        self.resumeButton.place_forget()
        self.patentActionflabel.place_forget()
        self.patentActionflabel_3.place(x=350, y=20)
        self.patentActionflabel_2.place (x=375, y=120)
        #self.userButton.place (x=375, y=440)
        self.patient_switch_enable()       
        
        
                
    def Load(self):
        self.patentActionflabel = tk.Label (self.frame, text='Increment Null Setting untill \nPatient Reports no fliker,\nPress resume when done',font=Font1,bg='white')
        self.patentActionflabel_3 = tk.Label (self.frame, text='IF Require\nVary NULL settings until\npatient reports on flicker',font=Font1,bg='white')
        self.brk_parf_label = tk.Label(self.content_frame,text='BRK FOVEA',bg="yellow", font= Font, width=12)  
        self.null_box =tk.Label(self.content_frame, text="NULL",
                                 font=('Helvetica', 24, 'bold'),
                                 bg='black', fg='#1210FF')
        self.content_frame.place(x=280, y=110, width=711, height=441)
        self.patentActionflabel_2 = tk.Label (self.frame, text='Patient\'s side Button \n Begins Traial',font=Font1,bg='white')
        self.null_box.place (x=100,y=20)
        self.trialList_min.place (x=450, y=60)
        self.brk_parf_label.place (x=500,y=10)
        self.trialList_mid.place (x=520, y=60)
        self.trialList_max.place (x=590, y=60)
        self.patentActionflabel.place(x=350, y=20)    
        self.trialList_mid.insert(0,160)
        self.create_side_buttons()

        self.header = HeaderComponent(
            self.frame,
            "Macular Densitometer                                                          BRK Fovea Test"
        )
        

        self.inc_dec_1 = False 
        self.inc_dec_2 = False  
        self.process_chainge = 0       

        self.DepthVal = tk.Label(self.content_frame, text="15",
                                   font=('Helvetica Rounded', 28, 'bold'),
                                   width=3, height=1,
                                   bg='#1f2836', fg='white',
                                   textvariable=str(self.depthVal))
        self.DepthVal.place(x=110,y=142)
        self.UPButton.place (x=110,  y=75)   
        self.DownButton.place (x=110,  y=200)
        self.saveButton.place_forget()
        #saveButton.place (x=100, y=340)
      
        #self.saveButton['state'] = tk.enable
                   

        self.resumeButton = tk.Button(self.frame,
                                 text="Resume",
                                 command=self.handleResume, font=Font, bg='Orange',
                                 width=10)

        self.resumeButton.place(x=resume_spot_x,y=resume_spot_y)


#         self.userButton = tk.Button(self.frame,
#                                  text="USER",
#                                  command=handleuser, font=Font, bg='Orange',
#                                  width=10)       

        
        def onfw():
            pageDisctonary['BrkFovea_1'].hide()
            pageDisctonary['CffParaFovea'].show()
            globaladc.get_print("no fw screen")

        def onbw():
            pageDisctonary['BrkFovea_1'].hide()
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



#     def Load(self):
#         self.patentActionflabel = tk.Label (self.frame, text='Increment Null Setting untill \nPatient Reports no fliker,\nPress resume when done',font=Font1,bg='white')
#         self.patentActionflabel_3 = tk.Label (self.frame, text='IF Require\nVary NULL settings until\npatient reports on flicker',font=Font1,bg='white')
#         self.brk_parf_label = tk.Label(self.frame,text='BRK FOVEA',bg="yellow", font= Font, width=12)  
#         self.null_box = tk.Label(self.frame,text='NULL',bg="white", font= Font, width=12)        
#         self.patentActionflabel_2 = tk.Label (self.frame, text='Patient\'s side Button \n Begins Traial',font=Font1,bg='white')
#         self.trialList_min.place (x=750, y=40)
#         self.null_box.place (x=100,y=20)
#         self.brk_parf_label.place (x=750,y=10)
#         self.trialList_mid.place (x=800, y=40)
#         self.trialList_max.place (x=850, y=40)
#         self.patentActionflabel.place(x=350, y=20)    
#         self.trialList_mid.insert(0,160)
        
#         self.inc_dec_1 = False 
#         self.inc_dec_2 = False  
#         self.process_chainge = 0       

#         self.DepthVal = tk.Label(self.frame,textvariable=str(self.depthVal),justify="center", font=Font, bg='white') 
#         self.DepthVal.place(x=120,y=130)
#         self.UPButton.place (x=110,  y=75)   
#         self.DownButton.place (x=110,  y=200)
#         self.saveButton.place_forget()
#         #saveButton.place (x=100, y=340)
      
#         #self.saveButton['state'] = tk.enable
                   

#         self.resumeButton = tk.Button(self.frame,
#                                  text="Resume",
#                                  command=self.handleResume, font=Font, bg='Orange',
#                                  width=10)

#         self.resumeButton.place(x=resume_spot_x,y=resume_spot_y)


# #         self.userButton = tk.Button(self.frame,
# #                                  text="USER",
# #                                  command=handleuser, font=Font, bg='Orange',
# #                                  width=10)       

        
#         def onfw():
#             pageDisctonary['BrkFovea_1'].hide()
#             pageDisctonary['CffParaFovea'].show()
#             globaladc.get_print("no fw screen")

#         def onbw():
#             pageDisctonary['BrkFovea_1'].hide()
#             pageDisctonary['MainScreen'].show()



#         fwButton = tk.Button (self.frame,
#                                  text=">>", font=Font2,
#                                  command=onfw, bg='Green',
#                                  width=10)
       
#         bwButton = tk.Button (self.frame,
#                                  text="<<", font=Font2,
#                                  command=onbw, bg='Green',
#                                  width=10)
  
#         # fwButton.place(x=620,y=500)
#         # bwButton.place(x=420, y=500)


    # def show(self):
    #     self.frame.place(width=1024,height=600)
    #     globaladc.brk_Fovea_Prepair()
    #     # globaladc.brk_fovea_1_screen_initialize() 			# run this while loding brk fovea 1st screen
    #     self.skip_event = True
    #     self.threadCreated=False
    #     self.run_therad()        
    #     self.process = 0
    #     self.value = 160
    #     self.pre_brk_mid = 160
    #     self.locate =0
    #     self.inc_dec_2 = False
    #     self.threadCreated =False
    #     leng = self.trialList_max.size()
    #     self.trialList_max.delete(0,leng-1)
    #     leng = self.trialList_min.size()
    #     self.trialList_min.delete(0,leng-1)
    #     leng = self.trialList_mid.size()
    #     self.trialList_mid.delete(0,leng-1)
    #     self.trialList_mid.insert(0,160)
    #     self.DepthVal.config(textvariable=str(self.depthVal))
    #     self.DepthVal.place(x=120,y=130)
    #     self.resumeButton.place(x=resume_spot_x,y=resume_spot_y)
    #     #self.userButton.place_forget()
    #     self.patentActionflabel.place(x=350, y=20)
    #     self.patentActionflabel_3.place_forget()
    #     self.patentActionflabel_2.place_forget ()
    #     self.UPButton.place(x=110, y=75)   
    #     self.DownButton.place(x=110, y=200)
    #     self.inc_dec_1 = False
    #     self.null_box.place (x=100,y=20)
    #     self.depthVal.set(1)
  



    def show(self):
        self.frame.place(width=1024,height=600)
        globaladc.brk_Fovea_Prepair()
        # globaladc.brk_fovea_1_screen_initialize() 			# run this while loding brk fovea 1st screen
        self.skip_event = True
        self.threadCreated=False
        self.run_therad()        
        self.process = 0
        self.value = 160
        self.pre_brk_mid = 160
        self.locate =0
        self.inc_dec_2 = False
        self.threadCreated =False
        leng = self.trialList_max.size()
        self.trialList_max.delete(0,leng-1)
        leng = self.trialList_min.size()
        self.trialList_min.delete(0,leng-1)
        leng = self.trialList_mid.size()
        self.trialList_mid.delete(0,leng-1)
        self.trialList_mid.insert(0,160)
        self.DepthVal.config(textvariable=str(self.depthVal))
        self.DepthVal.place(x=110,y=142)

        self.resumeButton.place(x=resume_spot_x,y=resume_spot_y)
        #self.userButton.place_forget()
        self.patentActionflabel.place(x=350, y=20)
        self.patentActionflabel_3.place_forget()
        self.patentActionflabel_2.place_forget ()
        self.UPButton.place(x=110, y=75)   
        self.DownButton.place(x=110, y=200)
        self.inc_dec_1 = False
        self.null_box.place (x=100,y=20)
        self.depthVal.set(1)
  



    def hide(self):
        self.stop_therad()
        self.frame.place_forget()
        
    
    def setRunTestScreen(self, runtestScreen):
        self.runtestScreen = runtestScreen

    def run_therad(self):
        globaladc.get_print("worker_brk_f thread started")
        self.worker_brk_f = PerodicThread.PeriodicThread(self.intervel,self)
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
                    #globaladc.buzzer_3()                    
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
                    #globaladc.buzzer_3()
                    self.trialList_min.delete(self.locate)
                    self.skip_event = True                   
                else : 
                    self.inc_dec_2 = False 
                    self.value = self.value - 1
                    self.trialList_min.delete(self.locate) 
                    self.trialList_min.insert(self.locate,self.value)                
        else :            
            globaladc.get_print('BF')
        globaladc.blue_led_Freq_control(self.value)


    def getName():
        return "BrkFovea_1"  