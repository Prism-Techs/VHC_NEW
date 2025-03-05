import tkinter as tk
from tkinter import Frame, ttk, messagebox
from Keyboard import KeyBoard
from FlikerScreen import flikerWindow
from MainWindow import mainWindow
from CFF_FOVEA import CffFovea
from CFF_PARA_FOVEA import CffParaFovea
from Admin import Admin
from BRK_FOVEA_1 import BrkFovea_1
from BRK_FOVEA_2 import BrkparaFovea
from globalvar import pageDisctonary, globaladc, currentPatientInfo
import os.path
import subprocess as sp
from login import LoginApp

Font = ("Arial", 20)
Font2 = ("Arial", 10)
x = 80

class StatrupClass:
    def __init__(self):
        self.window = tk.Tk()
        self.window.attributes('-fullscreen', True)
        self.window.geometry("1024x600")
        self.window.resizable(0, 0)
        self.window.configure(background='#64edb4')

        # Initialize frames
        self.main_frame = Frame(self.window, bg='#64edb4')
        self.fliker_frame = Frame(self.window, bg='#64edb4')
        self.cff_fovea_frame = Frame(self.window, bg='#64edb4')
        self.cff_para_fovea_frame = Frame(self.window, bg='#64edb4')
        self.brkf1_frame = Frame(self.window, bg='#64edb4')
        self.brkf2_frame = Frame(self.window, bg='#64edb4')
        self.admin_frame = Frame(self.window, bg='#64edb4')

        currentPatientInfo.log_update("System_Started")
        globaladc.fan_on()

        # Load all components
        self.mw = mainWindow(self.main_frame)
        self.fw = flikerWindow(self.fliker_frame)
        self.brkf_1 = BrkFovea_1(self.brkf1_frame)
        self.brkf_2 = BrkparaFovea(self.brkf2_frame)
        self.cff = CffFovea(self.cff_fovea_frame)
        self.cff_p = CffParaFovea(self.cff_para_fovea_frame)
        self.admin = Admin(self.admin_frame)
        self.login = LoginApp(self.window)

        # Initialize buttons
        self.setup_buttons()

    def setup_buttons(self):
        """Initialize and configure all buttons"""
        self.admin_button = tk.Button(self.window, text="Admin", command=self.handle_admin,
                                    font=Font, width=10)
        self.start_button = tk.Button(self.window, text="Start", command=self.handle_start,
                                    font=Font, bg='Green', width=10)
        self.fliker_demo_button = tk.Button(self.window, text="Flicker Demo",
                                          command=self.handle_flicker_demo, font=Font, width=10)
        self.home_screen_button = tk.Button(self.window, text="Home",
                                          command=self.handle_home_screen, font=Font, width=10)
        self.save_button = tk.Button(self.brkf1_frame, text="Save", bg='#a0f291',
                                   command=self.handle_save, font=Font, width=10)
        self.save_button_2 = tk.Button(self.brkf2_frame, text="Save", bg='#a0f291',
                                     command=self.handle_save_2, font=Font, width=10)

        self.brkf_1.saveButton = self.save_button
        self.brkf_2.saveButton = self.save_button_2

    # Button visibility methods
    def hide_start_button(self):
        self.start_button.place_forget()

    def show_start_button(self):
        self.start_button.place(x=x+220, y=500)

    def hide_admin_button(self):
        self.admin_button.place_forget()

    def show_admin_button(self):
        self.admin_button.place(x=x+10, y=500)

    def hide_fliker_button(self):
        self.fliker_demo_button.place_forget()

    def show_fliker_button(self):
        self.fliker_demo_button.place(x=x+420, y=500)

    def show_home_button(self):
        self.home_screen_button.place(x=820, y=500)

    def hide_home_button(self):
        self.home_screen_button.place_forget()

    # Screen management methods
    def hide_all(self):
        """Hide all screens and buttons"""
        self.mw.hide()
        self.fw.hide()
        self.cff.hide()
        self.cff_p.hide()
        self.brkf_1.hide()
        self.brkf_2.hide()
        self.admin.hide()
        self.login.root.withdraw()  # Hide login window
        self.hide_admin_button()
        self.hide_start_button()
        self.hide_fliker_button()
        self.hide_home_button()

    def show_login_screen(self):
        self.hide_all()
        self.login.load_ui()  # Load UI components
        self.login.show_ui()  # Show UI components
        self.login.root.deiconify()  # Show the login window
        currentPatientInfo.log_update("Enter_to_Login_screen")

    def show_main_screen(self):
        self.hide_all()
        self.show_admin_button()
        self.show_start_button()
        self.show_fliker_button()
        self.mw.show()
        currentPatientInfo.log_update("Enter_to_Main_screen")

    def show_fliker_screen(self):
        if not self.mw.ValidateUserInput():
            messagebox.showerror("USB Error", "Please enter User information")
            return
        self.hide_all()
        self.show_home_button()
        self.fw.show()
        globaladc.buzzer_1()
        currentPatientInfo.log_update("Enter_to_Flicker_screen")

    def show_test_run_screen(self):
        self.hide_all()
        self.show_home_button()
        self.cff.show()
        currentPatientInfo.log_update_pashent()
        currentPatientInfo.log_update("Enter_to_CFF_screen")

    def show_test_run_screen_2(self):
        self.hide_all()
        self.show_home_button()
        self.cff_p.show()
        currentPatientInfo.log_update("Enter_to_CFFP_screen")

    # Button handlers
    def handle_admin(self):
        globaladc.get_print("to be implemented")
        globaladc.buzzer_1()
        self.hide_all()
        self.show_home_button()
        self.admin.show()
        currentPatientInfo.log_update("Admin_pressed")

    def handle_start(self):
        if not self.mw.ValidateUserInput():
            globaladc.buzzer_1()
            messagebox.showerror("Data Error", "Please enter User information")
            return
        
        state = self.find_usb()
        if state == 'false':
            globaladc.buzzer_1()
            messagebox.showerror("USB Error", "Please check USB Drive\n(Name:-\“USB_DEVICE\”)\nInserted Properly \nif not, insert \nif inserted, remove and Re-insert")
            return

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
        self.show_test_run_screen()

    def handle_flicker_demo(self):
        globaladc.buzzer_1()
        self.show_fliker_screen()

    def handle_home_screen(self):
        globaladc.end_process()
        globaladc.skip_main_rset()
        globaladc.buzzer_1()
        sve = globaladc.get_save_no()
        if sve == 1:
            cff_fovea_frq = globaladc.get_cff_fovea_frq()
            currentPatientInfo.SetCFF_F(cff_fovea_frq)
            f_mpod = globaladc.get_cal_f_mpod()
            currentPatientInfo.SetF_mpod(f_mpod)
            state = self.find_usb()
            if state != 'false':
                globaladc.get_print('Save to file to ' + currentPatientInfo.Name + '.TXT')
                currentPatientInfo.Save_brk(state)
                pageDisctonary['BrkparaFovea'].hide()
                globaladc.put_save_no(0)
                self.show_main_screen()
            else:
                messagebox.showerror("USB Error", "Please check USB Drive Inserted Properly \nif not inserted, insert it wait for a second and Press SAVE once again \nif inserted, remove and Re-insert again Wait-a-while and Press SAVE once again")
                return
        else:
            currentPatientInfo.log_update("Home_pressed")
            self.show_main_screen()

    def handle_save(self):
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
            self.show_main_screen()
        else:
            messagebox.showerror("USB Error", "Please check USB Drive Inserted Properly \nif not inserted, insert it Wait-a-while and Press SAVE once again \nif inserted, remove and Re-insert wait for a second again and Press SAVE once again")

    def handle_save_2(self):
        cff_f = globaladc.get_cff_fovea_frq()
        currentPatientInfo.SetCFF_F(cff_f)
        globaladc.skip_main_rset()
        f_mpod = globaladc.get_cal_f_mpod()
        currentPatientInfo.SetF_mpod(f_mpod)
        cff_p = globaladc.get_cff_para_fovea_frq()
        currentPatientInfo.SetCFF_P(cff_p)
        f_sd = globaladc.get_cal_f_sd()
        currentPatientInfo.SetF_SD(f_sd)
        state = self.find_usb()
        if state != 'false':
            log_data = f"CFF_F-{cff_f},CFF_P-{cff_p},F_mpod-{f_mpod},F_SD-{f_sd}"
            currentPatientInfo.log_update(log_data)
            str_data = 'Save to file to ' + currentPatientInfo.Name + '.TXT'
            globaladc.get_print(str_data)
            self.brkf_2.saveButton.config(command=self.non, text="Busy", bg='#f24e79')
            currentPatientInfo.Save_brk_p(state)
            globaladc.all_led_off()
            pageDisctonary['BrkparaFovea'].hide()
            self.show_main_screen()
            self.brkf_2.saveButton.config(command=self.handle_save_2, text="Save", bg='#a0f291')
        else:
            messagebox.showerror("USB Error", "Please check USB Drive Inserted Properly \nif not inserted, insert it wait for a second and Press SAVE once again \nif inserted, remove and Re-insert again Wait-a-while and Press SAVE once again")

    def non(self):
        globaladc.get_print('non')

    def find_usb(self):
        output = sp.getoutput("df -x squashfs")
        poss = output.find("/media")
        if poss == -1:
            currentPatientInfo.log_update("Drive_not_inserted")
            return "false"
        return output[poss:]

    def main(self):
        globaladc.all_led_off()
        globaladc.fan_on()
        pageDisctonary["MainScreen"] = self.mw
        pageDisctonary["FlikerScreen"] = self.fw
        pageDisctonary["BrkFovea_1"] = self.brkf_1
        pageDisctonary["CffFovea"] = self.cff
        pageDisctonary["CffParaFovea"] = self.cff_p
        pageDisctonary["BrkparaFovea"] = self.brkf_2
        pageDisctonary["Admin"] = self.admin
        self.mw.Load()
        self.cff.Load()
        self.cff_p.Load()
        self.brkf_1.Load()
        self.brkf_2.Load()
        self.admin.Load()
        globaladc.buzzer_1()
        self.show_login_screen()  # Start with login screen
        self.window.mainloop()
        globaladc.buzzer_1()

if __name__ == "__main__":
    app = StatrupClass()
    app.main()