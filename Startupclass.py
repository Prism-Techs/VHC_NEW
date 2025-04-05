import tkinter as tk
from tkinter import Frame, ttk, messagebox
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
import os.path
import subprocess as sp
from header import HeaderComponent
from login import LoginApp
from Patient_checker import run_in_thread
from home_page import HomePage

Font = ("Arial", 20)
Font2 = ("Arial", 10)
x = 80

class StatrupClass:
    def HideStartButton(self):
        self.StartButton.place_forget()

    def ShowStartButton(self):
        self.StartButton.place(x=x+220, y=500)

    def HideAdminButton(self):
        self.AdminButton.place_forget()

    def ShowAdminButton(self):
        self.AdminButton.place(x=x+10, y=500)

    def HideFlikerButton(self):
        self.FlikerDemoButton.place_forget()

    def ShowFlikerButton(self):
        self.FlikerDemoButton.place(x=x+420, y=500)

    def ShowHomeButton(self):
        self.HomeScreenButton.place(x=820, y=500)

    def HideHomeButton(self):
        self.HomeScreenButton.place_forget()

    def __init__(self):
        self.window = tk.Tk()
        # self.window.attributes('-fullscreen', True)
        self.window.geometry("1024x600")
        self.window.resizable(0, 0)

        # Frames
        self.loginFrame = Frame(self.window, bg='black')
        self.homeFrame = Frame(self.window, bg="black")  # Fixed typo: homeFram -> homeFrame
        self.mainFrame = Frame(self.window, bg='#64edb4')
        self.flikerFrame = Frame(self.window, bg='black')
        self.cffFoveaFrame = Frame(self.window, bg='#64edb4')
        self.CffParaFoveaFrame = Frame(self.window, bg='#64edb4')
        self.brkf1Frame = Frame(self.window, bg='#64edb4')
        self.brkf2Frame = Frame(self.window, bg='#64edb4')
        self.adminFrame = Frame(self.window, bg='#64edb4')

        currentPatientInfo.log_update("System_Started")
        globaladc.fan_on()

        # Screen Instances
        self.hm = LoginApp(self.loginFrame, on_login_success=self.ShowHomeScreen)
        self.home = HomePage(self.homeFrame, self)
        self.mw = mainWindow(self.mainFrame)
        self.fw = flikerWindow(self.flikerFrame)
        self.brkf_1 = BrkFovea_1(self.brkf1Frame)
        self.brkf_2 = BrkparaFovea(self.brkf2Frame)
        self.cff = CffFovea(self.cffFoveaFrame)
        self.cffP = CffParaFovea(self.CffParaFoveaFrame)
        self.admin = Admin(self.adminFrame)
        self.header = HeaderComponent(self.window)

        run_in_thread('patient_data', 'https://vhcbeta-api.prismtechs.in/patient/sync/', 'wifi_status.json')

        # Buttons
        self.StartButton = tk.Button(self.window, text="Start", font=Font, command=self.handleStart, bg='Green', width=10)
        self.AdminButton = tk.Button(self.window, text="Admin", font=Font, command=self.handleAdmin, width=10)
        self.FlikerDemoButton = tk.Button(self.window, text="Flicker Demo", font=Font, command=self.handleFlikerDrmo, width=10)
        self.HomeScreenButton = tk.Button(self.window, text="Home", font=Font, command=self.ShowHomeScreen, width=10)
        self.saveButton = tk.Button(self.brkf1Frame, text="Save", bg='#a0f291', command=self.handleSave, font=Font, width=10)
        self.brkf_1.saveButton = self.saveButton
        self.saveButton_2 = tk.Button(self.brkf2Frame, text="Save", bg='#a0f291', command=self.handleSave_2, font=Font, width=10)
        self.brkf_2.saveButton = self.saveButton_2

    def main(self):
        globaladc.all_led_off()
        globaladc.fan_on()
        pageDisctonary["LoginScreen"] = self.hm
        pageDisctonary["HomeScreen"] = self.home
        pageDisctonary["MainScreen"] = self.mw
        pageDisctonary["FlikerScreen"] = self.fw
        pageDisctonary["BrkFovea_1"] = self.brkf_1
        pageDisctonary["CffFovea"] = self.cff
        pageDisctonary["CffParaFovea"] = self.cffP
        pageDisctonary["BrkparaFovea"] = self.brkf_2
        pageDisctonary["Admin"] = self.admin

        self.hm.Load()
        self.home.Load()
        self.mw.Load()
        self.fw.Load()
        self.cff.Load()
        self.cffP.Load()
        self.brkf_1.Load()
        self.brkf_2.Load()
        self.admin.Load()

        globaladc.buzzer_1()
        self.ShowLoginScreen()  # Start with Login Screen
        self.window.mainloop()
        globaladc.buzzer_1()

    def ShowLoginScreen(self):
        self.hm.show()
        self.home.hide()
        self.mw.hide()
        self.fw.hide()
        self.cff.hide()
        self.cffP.hide()
        self.brkf_1.hide()
        self.brkf_2.hide()
        self.admin.hide()
        self.HideStartButton()
        self.HideAdminButton()
        self.HideFlikerButton()
        self.HideHomeButton()
        currentPatientInfo.log_update("Enter_to_Login_screen")

    def ShowHomeScreen(self):
        globaladc.end_process()
        globaladc.skip_main_rset()
        globaladc.buzzer_1()
        sve = globaladc.get_save_no()
        if sve == 1:
            cff_fovea_frq = globaladc.get_cff_fovea_frq()
            currentPatientInfo.SetCFF_F(cff_fovea_frq)
            F_mpod = globaladc.get_cal_f_mpod()
            currentPatientInfo.SetF_mpod(F_mpod)
            state = self.find_usb()
            if state != 'false':
                globaladc.get_print('Save to file to ' + currentPatientInfo.Name + '.TXT')
                currentPatientInfo.Save_brk(state)
                globaladc.put_save_no(0)
            else:
                messagebox.showerror("USB Error", "Please check USB Drive...")
                return

        self.home.show()
        self.hm.hide()
        self.mw.hide()
        self.fw.hide()
        self.cff.hide()
        self.cffP.hide()
        self.brkf_1.hide()
        self.brkf_2.hide()
        self.admin.hide()
        self.ShowStartButton()
        # self.ShowAdminButton()
        self.HideAdminButton()

        self.ShowFlikerButton()
        self.HideHomeButton()
        currentPatientInfo.log_update("Enter_to_Home_screen")

    def ShowMainScreen(self):
        self.mw.show()
        self.hm.hide()
        self.home.hide()
        self.fw.hide()
        self.cff.hide()
        self.cffP.hide()
        self.brkf_1.hide()
        self.brkf_2.hide()
        self.admin.hide()
        self.ShowStartButton()
        self.HideAdminButton()
        self.ShowFlikerButton()
        self.ShowHomeButton()
        currentPatientInfo.log_update("Enter_to_Main_screen")

    def ShowFlikerScreen(self):
        if not self.mw.ValidateUserInput():
            messagebox.showerror("USB Error", "Please enter User information")
            return
        globaladc.buzzer_1()
        self.fw.show()
        self.hm.hide()
        self.home.hide()
        self.mw.hide()
        self.cff.hide()
        self.cffP.hide()
        self.brkf_1.hide()
        self.brkf_2.hide()
        self.admin.hide()
        self.HideAdminButton()
        self.HideStartButton()
        self.HideFlikerButton()
        self.ShowHomeButton()
        currentPatientInfo.log_update("Enter_to_Flicker_screen")

    def ShowTestRunScreen(self):
        self.cff.show()
        self.hm.hide()
        self.home.hide()
        self.mw.hide()
        self.fw.hide()
        self.cffP.hide()
        self.brkf_1.hide()
        self.brkf_2.hide()
        self.admin.hide()
        self.HideAdminButton()
        self.HideFlikerButton()
        self.HideStartButton()
        self.ShowHomeButton()
        currentPatientInfo.log_update_pashent()
        currentPatientInfo.log_update("Enter_to_CFF_screen")

    def ShowTestRunScreen_2(self):
        self.cffP.show()
        self.hm.hide()
        self.home.hide()
        self.mw.hide()
        self.fw.hide()
        self.cff.hide()
        self.brkf_1.hide()
        self.brkf_2.hide()
        self.admin.hide()
        self.HideAdminButton()
        self.HideFlikerButton()
        self.HideStartButton()
        self.ShowHomeButton()
        currentPatientInfo.log_update("Enter_to_CFFP_screen")

    def handleAdmin(self):
        globaladc.get_print("to be implemented")
        globaladc.buzzer_1()
        self.admin.show()
        self.hm.hide()
        self.home.hide()
        self.mw.hide()
        self.fw.hide()
        self.cff.hide()
        self.cffP.hide()
        self.brkf_1.hide()
        self.brkf_2.hide()
        self.HideAdminButton()
        self.HideFlikerButton()
        self.HideStartButton()
        self.ShowHomeButton()
        currentPatientInfo.log_update("Admin_pressed")

    def handleStart(self):
        if not self.mw.ValidateUserInput():
            globaladc.buzzer_1()
            messagebox.showerror("Data Error", "Please enter User information")
            return
        state = self.find_usb()
        if state == 'false':
            globaladc.buzzer_1()
            messagebox.showerror("USB Error", "Please check USB Drive\n(Name:-\“USB_DEVICE\”)\nInserted Properly \nif not, insert \nif inserted, remove and Re-insert")
            return

        self.mw.update_current_patient_info()
        if not self.mw.save_patient_data(show_message=False):
            messagebox.showerror("Save Error", "Failed to save patient data")
            return

        globaladc.buzzer_3()
        currentPatientInfo.log_update("Start_pressed")
        self.ShowTestRunScreen()

    def handleFlikerDrmo(self):
        self.ShowFlikerScreen()

    def find_usb(self):
        output = sp.getoutput("df -x squashfs")
        poss = output.find("/media")
        if poss == -1:
            currentPatientInfo.log_update("Drive_not_inserted")
            return "false"
        else:
            return output[poss:]

    def handleSave(self):
        cff_fovea_frq = globaladc.get_cff_fovea_frq()
        globaladc.skip_main_rset()
        currentPatientInfo.SetCFF_F(cff_fovea_frq)
        state = self.find_usb()
        if state != 'false':
            str_data = 'Save to file to ' + currentPatientInfo.Name + '.TXT'
            globaladc.get_print(str_data)
            if self.brkf_1.depthVal.get() == 0:
                log_data = "CFF_F-" + str(cff_fovea_frq) + ",F_mpod-0.00"
                currentPatientInfo.log_update(log_data)
                currentPatientInfo.Save_brk_0(state)
            elif self.brkf_1.depthVal.get() == 19:
                currentPatientInfo.Save_brk_19(state)
                log_data = "CFF_F-" + str(cff_fovea_frq) + ",F_mpod-+1.00"
                currentPatientInfo.log_update(log_data)
            globaladc.black_screen_initialize()
            pageDisctonary['BrkFovea_1'].hide()
            self.ShowHomeScreen()  # Return to Home Screen after save
        else:
            messagebox.showerror("USB Error", "Please check USB Drive Inserted Properly \nif not inserted, insert it Wait-a-while and Press SAVE once again \nif inserted, remove and Re-insert wait for a second again and Press SAVE once again")

    def handleSave_2(self):
        cff_F = globaladc.get_cff_fovea_frq()
        currentPatientInfo.SetCFF_F(cff_F)
        globaladc.skip_main_rset()
        F_mpod = globaladc.get_cal_f_mpod()
        currentPatientInfo.SetF_mpod(F_mpod)
        cff_p = globaladc.get_cff_para_fovea_frq()
        currentPatientInfo.SetCFF_P(cff_p)
        F_SD = globaladc.get_cal_f_sd()
        currentPatientInfo.SetF_SD(F_SD)
        currentPatientInfo.update_json()
        state = self.find_usb()
        if state != 'false':
            log_data = f"CFF_F-{cff_F},CFF_P-{cff_p},F_mpod-{F_mpod},F_SD-{F_SD}"
            currentPatientInfo.log_update(log_data)
            str_data = 'Save to file to ' + currentPatientInfo.Name + '.TXT'
            globaladc.get_print(str_data)
            self.brkf_2.saveButton.config(command=lambda: globaladc.get_print('non'), text="Busy", bg='#f24e79')
            currentPatientInfo.Save_brk_p(state)
            globaladc.all_led_off()
            pageDisctonary['BrkparaFovea'].hide()
            self.ShowHomeScreen()  # Return to Home Screen after save
            self.brkf_2.saveButton.config(command=self.handleSave_2, text="Save", bg='#a0f291')
        else:
            messagebox.showerror("USB Error", "Please check USB Drive Inserted Properly \nif not inserted, insert it wait for a second and Press SAVE once again \nif inserted, remove and Re-insert again Wait-a-while and Press SAVE once again")

if __name__ == "__main__":
    app = StatrupClass()
    app.main()