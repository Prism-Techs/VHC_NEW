import tkinter as tk
from tkinter import Frame, ttk
from tokenize import String
from Keyboard import KeyBoard
from FlikerScreen import flikerWindow
from MainWindow import mainWindow
from CFF_FOVEA import CffFovea
from CFF_PARA_FOVEA import CffParaFovea
from Admin import Admin
from BRK_FOVEA_1 import BrkFovea_1
from BRK_FOVEA_2 import BrkparaFovea
from globalvar import pageDisctonary
from globalvar import globaladc
from globalvar import currentPatientInfo
from tkinter import messagebox
import os.path
import subprocess as sp
from header import HeaderComponent
from login import LoginApp
from Patient_checker import run_in_thread




Font =  ("Arial",20)
Font2 = ("Arial",10)
x = 80

class StatrupClass:
    def HideStartButton(self):
        self.StartButton.place_forget()

    def ShowStartButton(self):
        self.StartButton.place (x=x+220, y=500)

    def HideAdminButton(self):
        self.AdminButton.place_forget()

    def ShowAdminButton(self):
        self.AdminButton.place (x=x+10, y=500)

    def HideFlikerButton(self):
        self.FlikerDemoButton.place_forget()

    def ShowFlikerButton(self):
        self.FlikerDemoButton.place (x=x+420, y=500)

    def ShowHomeButton(self):
        self.HomeScreenButton.place (x=820,y=500)  

    def HideHomeButton(self):
        self.HomeScreenButton.place_forget()        

    def __init__(self) -> None:        
        self.window = tk.Tk ()
        self.window.attributes('-fullscreen', True) 
        self.window.geometry ("1024x600")
        self.window.resizable (0, 0)
        # self.window.configure(background='#64edb4')
        self.mainFrame = Frame(self.window) 
        self.flikerFrame = Frame(self.window)
        self.cffFoveaFrame = Frame(self.window)
        self.CffParaFoveaFrame = Frame(self.window)
        self.brkf1Frame =  Frame(self.window)
        self.brkf2Frame = Frame(self.window)
        self.adminFrame = Frame(self.window)
        currentPatientInfo.log_update("System_Started")        
        self.mainFrame.config(bg='#64edb4')
        self.flikerFrame.config(bg='#64edb4')
        self.cffFoveaFrame.config(bg='#64edb4')
        self.CffParaFoveaFrame.config(bg='#64edb4')
        self.brkf1Frame.config(bg='#64edb4')
        self.brkf2Frame.config(bg='#64edb4')
        self.adminFrame.config(bg='#64edb4')
        globaladc.fan_on()
        #load all the frames
        self.mw = mainWindow(self.mainFrame)
        self.fw = flikerWindow(self.flikerFrame)
        self.brkf_1 = BrkFovea_1(self.brkf1Frame)
        self.brkf_2 = BrkparaFovea(self.brkf2Frame)
        self.cff = CffFovea(self.cffFoveaFrame)
        self.cffP =CffParaFovea(self.CffParaFoveaFrame)
        self.admin = Admin(self.adminFrame)
        self.header = HeaderComponent(self.window)

        #added the dev
        self.loginFrame = Frame(self.window, bg='black')
        self.homeFram = Frame(self.window,bg="black")
        self.hm = LoginApp(self.loginFrame)

        run_in_thread('patient_data','https://vhcbeta-api.prismtechs.in/patient/sync/','wifi_status.json')
   
        #intialize the buttons
        def handleAdmin():
            globaladc.get_print ("tobe implemented")
            globaladc.buzzer_1()
            self.ShowHomeButton()
            self.admin.show()
            self.HideAdminButton()
            self.HideFlikerButton()
            self.HideStartButton()
            currentPatientInfo.log_update("Admin_pressed")

        self.AdminButton = tk.Button (self.window,
                                    text="Admin",
                                    command=handleAdmin, font=Font,
                                    width=10)


        # def handleStart():            
        #     if self.mw.ValidateUserInput() == False :
        #         globaladc.buzzer_1()
        #         messagebox.showerror("Data Error","Please enter User information")
        #         return
        #     state=self.find_usb()       
        #     if state == 'false':
        #         globaladc.buzzer_1()
        #         messagebox.showerror("USB Error","Please check USB Drive\n(Name:-\“USB_DEVICE\”)\nInserted Properly \nif not, insert \nif inserted, remove and Re-insert")
        #         return
        #     globaladc.buzzer_1()
        #     MsgBox = messagebox.askquestion ('Alchohol Status','Do you consume\nAlchohol',icon = 'question')
        #     if MsgBox == 'yes':
        #        currentPatientInfo.setAlchohol_state("Y")
        #     else:                
        #         currentPatientInfo.setAlchohol_state("N")
        #     globaladc.buzzer_1()    
        #     MsgBox = messagebox.askquestion ('Smoking Status','Do you have habbit of\nSmoking',icon = 'question')
        #     if MsgBox == 'yes':
        #        currentPatientInfo.setSmoking_state("Y")
        #     else:                
        #         currentPatientInfo.setSmoking_state("N")
        #     globaladc.buzzer_1()
        #     MsgBox = messagebox.askquestion ('Diabetes Status','Are you suffering from\n Diabetes(Sugar)',icon = 'question')
        #     if MsgBox == 'yes':
        #        currentPatientInfo.setDiabetes_state("Y")
        #     else:                
        #         currentPatientInfo.setDiabetes_state("N")
        #     globaladc.buzzer_1()
        #     MsgBox = messagebox.askquestion ('Hypertension Status','Are you suffering from\nHypertension (BP)',icon = 'question')
        #     if MsgBox == 'yes':
        #        currentPatientInfo.setHypertension_state("Y")
        #     else:                
        #         currentPatientInfo.setHypertension_state("N")
        #     globaladc.buzzer_3()
        #     currentPatientInfo.log_update("Start_pressed")
        #     self.ShowTestRunScreen()
            

        def handleStart():
            if not self.mw.ValidateUserInput():
                globaladc.buzzer_1()
                messagebox.showerror("Data Error", "Please enter User information")
                return
            
            state = self.find_usb()
            if state == 'false':
                globaladc.buzzer_1()
                messagebox.showerror("USB Error", "Please check USB Drive\n(Name:-\“USB_DEVICE\”)\nInserted Properly \nif not, insert \nif inserted, remove and Re-insert")
                return

            # Load data directly from mainWindow UI instead of pop-ups
            globaladc.buzzer_1()
            currentPatientInfo.setAlchohol_state("Y" if self.mw.alcohol_var.get() == "Yes" else "N")
            
            globaladc.buzzer_1()
            currentPatientInfo.setSmoking_state("Y" if self.mw.smoking_var.get() == "Yes" else "N")
            
            globaladc.buzzer_1()
            currentPatientInfo.setDiabetes_state("Y" if self.mw.diabetes_var.get() == "Yes" else "N")
            
            globaladc.buzzer_1()
            currentPatientInfo.setHypertension_state("Y" if self.mw.bp_var.get() == "Yes" else "N")

            globaladc.buzzer_3()
            currentPatientInfo.log_update("Start_pressed")
            self.ShowTestRunScreen()    

        self.StartButton = tk.Button (self.window,
                                    text="Start", font=Font,
                                    command=handleStart, bg='Green',
                                    width=10)

        
            
        self.FlikerDemoButton = tk.Button (self.window,
                                text="Flicker Demo",
                                command=self.handleFlikerDrmo,font=Font,
                                width=10)

        self.HomeScreenButton = tk.Button (self.window,
                                text="Home",
                                command=self.handleHomeScreen,font=Font,
                                width=10)

        
        
        self.saveButton = tk.Button (self.brkf1Frame,
                                 text="Save",bg='#a0f291',
                                 command=self.handleSave, font=Font,
                                 width=10)
        self.brkf_1.saveButton = self.saveButton
        
        self.saveButton_2 = tk.Button (self.brkf2Frame,
                                text="Save",bg='#a0f291',
                                command=self.handleSave_2, font=Font,
                                width=10)
        self.brkf_2.saveButton = self.saveButton_2
        
        
    def main(self):
        globaladc.all_led_off()
        globaladc.fan_on()
        pageDisctonary["MainScreen"] = self.mw        
        pageDisctonary["FlikerScreen"] = self.fw
        pageDisctonary["BrkFovea_1"] = self.brkf_1
        pageDisctonary["CffFovea"] = self.cff
        pageDisctonary["CffParaFovea"] = self.cffP
        pageDisctonary["BrkparaFovea"] = self.brkf_2    
        pageDisctonary["Admin"] = self.admin
        self.mw.Load()
        # self.fw.Load()
        self.hm.Load()
        self.cff.Load()
        self.cffP.Load()
        self.brkf_1.Load()
        self.brkf_2.Load()
        self.admin.Load()  
        globaladc.buzzer_1()      
        self.ShowMainScreen()
        # self.hm.load_ui()
        self.window.mainloop()
        globaladc.buzzer_1()


        
        
            

        #fliker Deom  
    def handleFlikerDrmo(self):
        globaladc.buzzer_1()
        self.ShowFlikerScreen()


    def handleHomeScreen(self):
        globaladc.end_process()
        globaladc.skip_main_rset()
        globaladc.buzzer_1()
        sve= globaladc.get_save_no()        
        if sve == 1 :
            home=0
            cff_fovea_frq=globaladc.get_cff_fovea_frq()
            currentPatientInfo.SetCFF_F(cff_fovea_frq)        
            F_mpod = globaladc.get_cal_f_mpod()
            currentPatientInfo.SetF_mpod(F_mpod)
            #make same for home screen        
            #state=os.path.isdir('/media/pi/USB_DEVICE')        
            state=self.find_usb()
            if(state!= 'false'):      
                globaladc.get_print('Save to file to' + currentPatientInfo.Name+'.TXT')            
                #self.patient_switch_desable()
                currentPatientInfo.Save_brk(state)
                pageDisctonary['BrkparaFovea'].hide()
                globaladc.put_save_no(0)
                self.ShowMainScreen()                
            else:
                messagebox.showerror("USB Error","Please check USB Drive Inserted Properly \nif not inserted, insert it wait for a second and Press SAVE once again \nif inserted, remove and Re-insert again Wait-a-while and Press SAVE once again")
                return
        else:
            currentPatientInfo.log_update("Home_pressed")
            self.ShowMainScreen()

            
            
           

            #intial work flow show Main Screen
    def ShowMainScreen(self):  
        #globaladc.buzzer_1()
        # self.ShowAdminButton()
        # self.ShowStartButton()
        # self.ShowFlikerButton()
        self.HideHomeButton()
        # self.fw.hide()
        self.cff.hide()
        self.cffP.hide()
        self.brkf_1.hide()
        self.admin.hide()
        self.mw.hide()
        self.hm.show()
        currentPatientInfo.log_update("Enter_to_Main_screeen")
        # globaladc.main_Prepair() # run this while loading main Screen

    def ShowFlikerScreen(self):
        if self.mw.ValidateUserInput() == False :
                    messagebox.showerror("USB Error","Please enter User information")
                    return                        
        globaladc.buzzer_1()
        self.HideAdminButton()
        self.HideStartButton()
        self.HideFlikerButton()
        self.ShowHomeButton()
        # self.fw.show()
        self.cff.hide()
        self.admin.hide()
        self.mw.hide()
        currentPatientInfo.log_update("Enter_to_Flicker_screeen")

    def ShowTestRunScreen(self):  
        #globaladc.buzzer_1()
        self.HideAdminButton()
        self.HideFlikerButton()
        self.HideStartButton()
        self.ShowHomeButton()
        # self.fw.hide()
        self.mw.hide()
        self.cff.show()
        self.cffP.hide()
        self.admin.hide()
        currentPatientInfo.log_update_pashent()
        currentPatientInfo.log_update("Enter_to_CFF_screeen")
                

    def ShowTestRunScreen_2(self):  
        #globaladc.buzzer_1()
        self.HideAdminButton()
        self.HideFlikerButton()
        self.HideStartButton()
        self.ShowHomeButton()        
        # self.fw.hide()
        self.mw.hide()
        self.cff.hide()
        self.cffP.show()        
        self.ShowMainScreen()
        self.admin.hide()
        currentPatientInfo.log_update("Enter_to_CFFP_screeen")
        
        
    def find_usb(self):        
        output = sp.getoutput("df -x squashfs")    
        poss=output.find("/media")    
        if poss == -1:
            return("false")
            currentPatientInfo.log_update("Drive_not_inserted")
        else :
            out =output[poss:]
            return(out)
        
    def handleSave(self):
        cff_fovea_frq=globaladc.get_cff_fovea_frq()
        globaladc.skip_main_rset()
        currentPatientInfo.SetCFF_F(cff_fovea_frq)        
        #state=os.path.isdir('/media/pi/USB_DEVICE')        
        state=self.find_usb()
        if(state!= 'false'):
            str_data = 'Save to file to' + currentPatientInfo.Name + '.TXT'
            globaladc.get_print(str_data)             
            if self.brkf_1.depthVal.get() == 0:
                log_data = "CFF_F-"+str(cff_fovea_frq)+",F_mpod-0.00"
                currentPatientInfo.log_update(log_data)
                currentPatientInfo.Save_brk_0(state) 
            elif self.brkf_1.depthVal.get() == 19: 
                currentPatientInfo.Save_brk_19(state)
                log_data = "CFF_F-"+str(cff_fovea_frq)+",F_mpod-+1.00"
                currentPatientInfo.log_update(log_data)
            globaladc.black_screen_initialize()
            pageDisctonary['BrkFovea_1'].hide()
            self.ShowMainScreen
        else:
            messagebox.showerror("USB Error","Please check USB Drive Inserted Properly \nif not inserted, insert it Wait-a-while and Press SAVE once again \nif inserted, remove and Re-insert wait for a second again and Press SAVE once again")
            return
        # globaladc.main_screen_initialize()
        
    def non (self):
            globaladc.get_print('non')
        
    def handleSave_2(self):
        cff_F=globaladc.get_cff_fovea_frq()
        currentPatientInfo.SetCFF_F(cff_F)       
        globaladc.skip_main_rset()
        F_mpod=globaladc.get_cal_f_mpod()
        currentPatientInfo.SetF_mpod(F_mpod)
        
        cff_p=globaladc.get_cff_para_fovea_frq()
        currentPatientInfo.SetCFF_P(cff_p)
        
        F_SD=globaladc.get_cal_f_sd()
        currentPatientInfo.SetF_SD(F_SD)
        
        #make same for home screen        
        state=os.path.isdir('/media/pi/USB_DEVICE')        
        state=self.find_usb()
        if(state!= 'false'):
            log_data = "CFF_F-"+str(cff_F)+",CFF_P-"+str(cff_p)+",F_mpod-"+str(F_mpod)+",F_SD-"+str(F_SD)
            currentPatientInfo.log_update(log_data)
            str_data = 'Save to file to' + currentPatientInfo.Name +'.TXT'
            globaladc.get_print(str_data)            
            #self.patient_switch_desable()
            self.brkf_2.saveButton.config(command=self.non,text="Bussey",bg='#f24e79')
            currentPatientInfo.Save_brk_p(state)
            globaladc.all_led_off()
            pageDisctonary['BrkparaFovea'].hide()
            self.ShowMainScreen()
            self.brkf_2.saveButton.config(command=self.handleSave_2,text="Save",bg='#a0f291')
        else:
            messagebox.showerror("USB Error","Please check USB Drive Inserted Properly \nif not inserted, insert it wait for a second and Press SAVE once again \nif inserted, remove and Re-insert again Wait-a-while and Press SAVE once again")
            return
        # globaladc.main_Prepair()
        
