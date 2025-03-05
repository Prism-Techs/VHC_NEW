import tkinter as tk
from tkinter import Frame, ttk, messagebox
from datetime import datetime
import json
import os
from header import HeaderComponent
from Keyboard import KeyBoard
from FlikerScreen import flikerWindow
from MainWindow import mainWindow
from CFF_FOVEA import CffFovea
from CFF_PARA_FOVEA import CffParaFovea
from Admin import Admin
from BRK_FOVEA_1 import BrkFovea_1
from BRK_FOVEA_2 import BrkparaFovea
from globalvar import pageDisctonary, globaladc, currentPatientInfo
import subprocess as sp
from database import DatabaseConnection

Font = ("Arial", 20)
Font2 = ("Arial", 10)
x = 80

# LoginApp Class
class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.configure(bg='black')
        self.kb = KeyBoard()
        self.wifi_window = None
        self.password_visible = False
        self.json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "user_data")
        if not os.path.exists(self.json_path):
            os.makedirs(self.json_path)
        self.load_ui()

    def load_ui(self):
        self.header = HeaderComponent(self.root, "                                                       Macular Densitometer")
        self.content_frame = tk.Frame(self.root, bg='#1f2836', highlightbackground='white', highlightthickness=1)
        self.username = tk.Entry(self.content_frame, font=('Helvetica', 18), bg='#334155', fg='#94a3b8', insertbackground='white')
        self.username.insert(0, "Username")
        self.password = tk.Entry(self.content_frame, font=('Helvetica', 18), bg='#334155', fg='#94a3b8', insertbackground='white', show='*')
        self.password.insert(0, "Password")
        self.toggle_btn = tk.Button(self.content_frame, text="Show", font=('Arial', 12), bg='#334155', fg='white', bd=0,
                                  highlightthickness=0, activebackground='#334155', activeforeground='#42A5F5', cursor="hand2",
                                  command=self.toggle_password)
        self.mode_label = tk.Label(self.content_frame, text="Operation Mode", font=('Helvetica Neue', 18, 'bold'), bg='#1f2836', fg='white')
        self.operation_mode = tk.StringVar(value="Clinic")
        self.radio_frame = tk.Frame(self.content_frame, bg='#1f2836')
        self.radio_buttons = {}
        radio_style = {'font': ('Helvetica Neue', 12, 'bold'), 'fg': 'white', 'selectcolor': '#42A5F5', 'padx': 20,
                       'variable': self.operation_mode, 'height': 2, 'width': 10, 'indicatoron': 0}
        modes = [("Eye Camp", "Eye Camp"), ("Clinic", "Clinic"), ("Demo", "Demo")]
        for text, mode in modes:
            rb = tk.Radiobutton(self.radio_frame, text=text, value=mode, bg='#1f2836', activebackground='#1f2836', **radio_style)
            self.radio_buttons[mode] = rb
        self.login_btn = tk.Button(self.content_frame, text="LOGIN", font=('Arial', 24, 'bold'), bg='#1f2836', fg='white', bd=1,
                                 relief='solid', command=self.handle_login)
        self.time_label = tk.Label(self.root, font=('Helvetica Neue', 10), bg='black', fg='white')
        self.date_label = tk.Label(self.root, font=('Helvetica Neue', 10), bg='black', fg='white')

    def show_ui(self):
        self.header.set_wifi_callback(self.open_wifi_page)
        self.content_frame.place(x=200, y=115, width=624, height=430)
        self.username.place(x=62, y=50, width=500, height=61)
        self.username.bind('<FocusIn>', lambda e: self.on_entry_click(self.username, "Username"))
        self.username.bind('<FocusOut>', lambda e: self.on_focus_out(self.username, "Username"))
        self.password.place(x=62, y=140, width=500, height=61)
        self.password.bind('<FocusIn>', lambda e: self.on_entry_click(self.password, "Password"))
        self.password.bind('<FocusOut>', lambda e: self.on_focus_out(self.password, "Password"))
        self.toggle_btn.place(x=520, y=150, width=40, height=40)
        self.mode_label.place(x=112, y=210, width=400, height=71)
        frame_width = 491
        content_width = 624
        x_start = (content_width - frame_width) // 2
        self.radio_frame.place(x=x_start, y=270, width=frame_width, height=49)
        button_width = 158
        total_width = len(self.radio_buttons) * button_width
        start_x = (frame_width - total_width) // 2
        for i, (mode, rb) in enumerate(self.radio_buttons.items()):
            x_pos = start_x + (i * button_width)
            rb.place(x=x_pos, y=0)
        self.operation_mode.trace('w', self.update_radio_styles)
        self.update_radio_styles()
        self.login_btn.place(x=230, y=350, width=161, height=51)
        self.login_btn.bind('<Enter>', self.on_login_hover)
        self.login_btn.bind('<Leave>', self.on_login_leave)
        self.time_label.place(x=960, y=550)
        self.date_label.place(x=934, y=570)
        self.update_datetime()

    def update_radio_styles(self, *args):
        selected_value = self.operation_mode.get()
        for value, rb in self.radio_buttons.items():
            if value == selected_value:
                rb.configure(bg='#42A5F5', activebackground='#42A5F5', fg='white')
            else:
                rb.configure(bg='#1f2836', activebackground='#1f2836', fg='white')

    def on_login_hover(self, event):
        self.login_btn.configure(bg='#42A5F5', fg='white')

    def on_login_leave(self, event):
        self.login_btn.configure(bg='#1f2836', fg='white')

    def update_datetime(self):
        current_time = datetime.now().strftime('%H:%M')
        current_date = datetime.now().strftime('%d-%m-%Y')
        self.time_label.config(text=current_time)
        self.date_label.config(text=current_date)
        self.root.after(1000, self.update_datetime)

    def on_entry_click(self, entry, default_text):
        current_text = entry.get().strip()
        if current_text == default_text:
            entry.delete(0, tk.END)
            entry.configure(fg='white')
            if entry == self.password and current_text != "Password":
                entry.configure(show='*')
        self.kb.createAlphaKey(self.root, entry)

    def on_focus_out(self, entry, default_text):
        current_text = entry.get().strip()
        if current_text == '':
            entry.delete(0, tk.END)
            entry.insert(0, default_text)
            entry.configure(fg='#94a3b8')
            if entry == self.password:
                entry.configure(show='')

    def toggle_password(self):
        self.password_visible = not self.password_visible
        if self.password_visible:
            self.password.configure(show='')
            self.toggle_btn.configure(text='Hide', fg='#42A5F5')
        else:
            self.password.configure(show='*')
            self.toggle_btn.configure(text='Show', fg='white')

    def open_wifi_page(self):
        print("Opening WiFi page")

    def generate_user_json(self, user_data, operation_mode):
        try:
            user_info = {
                "username": user_data['username'],
                "first_name": user_data['first_name'],
                "last_name": user_data['last_name'],
                "title": user_data['title'] if user_data['title'] else "",
                "login_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "is_doctor": user_data['is_doctor'],
                "is_operator": user_data['is_operator'],
                "user_id": user_data['id'],
                'operation_mode': operation_mode
            }
            filename = f"user_{user_data['username']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            filepath = os.path.join(self.json_path, filename)
            with open(filepath, 'w') as json_file:
                json.dump(user_info, json_file, indent=4)
            latest_filepath = os.path.join(self.json_path, "latest_user.json")
            with open(latest_filepath, 'w') as json_file:
                json.dump(user_info, json_file, indent=4)
            return filepath
        except Exception as e:
            print(f"Error generating user JSON: {e}")
            return None

    def handle_login(self):
        username = self.username.get()
        password = self.password.get()
        if username in ["", "Username"] or password in ["", "Password"]:
            self.root.update()
            x = self.root.winfo_x() + self.root.winfo_width()//2 - 100
            y = self.root.winfo_y() + self.root.winfo_height()//2 - 50
            messagebox.showerror("Error", "Please enter both username and password")
            return
        self.db = DatabaseConnection()
        self.db.connect()
        user = self.db.verify_login(username, password)
        if user:
            json_file = self.generate_user_json(user, self.operation_mode.get())
            if json_file:
                self.root.update()
                x = self.root.winfo_x() + self.root.winfo_width()//2 - 100
                y = self.root.winfo_y() + self.root.winfo_height()//2 - 50
                messagebox.showinfo("Success",
                                f'Welcome {user["title"] + " " if user["title"] else ""}{user["first_name"]} {user["last_name"]}',
                                parent=self.root)
                self.root.withdraw()
                if hasattr(self, 'callback') and callable(self.callback):
                    self.callback()  # Transition to HomePage
            else:
                self.root.update()
                x = self.root.winfo_x() + self.root.winfo_width()//2 - 100
                y = self.root.winfo_y() + self.root.winfo_height()//2 - 50
                messagebox.showwarning("Warning", 'Login successful but failed to save user data')
        else:
            self.root.update()
            x = self.root.winfo_x() + self.root.winfo_width()//2 - 100
            y = self.root.winfo_y() + self.root.winfo_height()//2 - 50
            messagebox.showerror("Error", 'Invalid username or password')

# HomePage Class
class HomePage:
    def __init__(self, root, startup_instance):
        self.root = root
        self.startup = startup_instance
        self.buttons = []
        self.colors = {'bg_black': 'black', 'fg_white': 'white', 'button_normal': '#101826', 'button_hover': '#2196F3', 'button_hover_fg': '#64B5F6'}
        self.fonts = {'welcome': ('Helvetica Neue', 14, 'bold'), 'datetime': ('Helvetica Neue', 12), 'button': ('Arial', 20, 'bold')}
        self.time_update_interval = 10000
        self.root.geometry("1024x600")
        self.root.resizable(False, False)
        self.root.configure(bg=self.colors['bg_black'])
        self.root.overrideredirect(True)
        self.load_ui()

    def load_ui(self):
        self.header = HeaderComponent(self.root, "                                                    Home Page")
        self.user_info_label = tk.Label(self.root, text="Welcome", font=self.fonts['welcome'], fg=self.colors['fg_white'],
                                      bg=self.colors['bg_black'], anchor='w')
        self.button_configs = [("Create User", self.create_user), ("View Reports", self.view_reports), ("Test Mode", self.test_mode), ("Logout", self.logout)]
        self.buttons = []
        for text, command in self.button_configs:
            button = tk.Button(self.root, text=text, command=command, font=self.fonts['button'], bg=self.colors['button_normal'],
                             fg=self.colors['fg_white'], bd=1, relief='solid', width=15, height=1)
            self.buttons.append(button)
        self.time_label = tk.Label(self.root, font=self.fonts['datetime'], fg=self.colors['fg_white'], bg=self.colors['bg_black'])
        self.date_label = tk.Label(self.root, font=self.fonts['datetime'], fg=self.colors['fg_white'], bg=self.colors['bg_black'])

    def show_ui(self):
        self.header.set_wifi_callback(self.switch_to_wifi)
        self.user_info_label.place(x=20, y=150, width=280, height=40)
        y_positions = [150, 250, 350, 450]
        for i, button in enumerate(self.buttons):
            button.place(x=382, y=y_positions[i])
            button.bind('<Enter>', lambda e, b=button: b.config(bg=self.colors['button_hover'], fg=self.colors['button_hover_fg'], bd=2))
            button.bind('<Leave>', lambda e, b=button: b.config(bg=self.colors['button_normal'], fg=self.colors['fg_white'], bd=1))
        self.time_label.place(x=900, y=560)
        self.date_label.place(x=900, y=580)
        self.update_datetime()
        self.check_user_role()
        self.root.deiconify()

    def hide_ui(self):
        self.root.withdraw()

    def update_datetime(self):
        current = datetime.now()
        self.time_label.config(text=current.strftime('%H:%M'))
        self.date_label.config(text=current.strftime('%d-%m-%Y'))
        self.root.after(self.time_update_interval, self.update_datetime)

    def switch_to_wifi(self):
        if "WifiSettings" not in pageDisctonary:
            wifi_frame = tk.Frame(self.root, bg='#64edb4')
            pageDisctonary["WifiSettings"] = WifiSettings(wifi_frame, self.startup)
            pageDisctonary["WifiSettings"].Load()
        self.startup.hide_all()
        self.startup.show_home_button()
        pageDisctonary["WifiSettings"].show()

    def create_user(self):
        messagebox.showinfo("Action", "Create User functionality to be implemented")
        print("Create user clicked")

    def view_reports(self):
        messagebox.showinfo("Action", "View Reports functionality to be implemented")
        print("View reports clicked")

    def test_mode(self):
        self.hide_ui()
        self.startup.show_test_run_screen()

    def logout(self):
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.hide_ui()
            self.startup.show_login_screen()
            print("Logout clicked")

    def get_user_data_path(self):
        return os.path.join(os.path.dirname(os.path.realpath(__file__)), "user_data", "latest_user.json")

    def check_user_role(self):
        try:
            json_path = self.get_user_data_path()
            if os.path.exists(json_path):
                with open(json_path, 'r') as file:
                    user_data = json.load(file)
                is_operator = user_data.get('is_operator', 0) == 1
                self.update_user_info(user_data)
                self.update_button_visibility(is_operator)
            else:
                self.user_info_label.config(text="Welcome,\nGuest")
                self.update_button_visibility(False)
                messagebox.showwarning('Warning', 'No user data found. Running as Guest.')
        except (json.JSONDecodeError, FileNotFoundError) as e:
            self.user_info_label.config(text="Welcome,\nGuest")
            self.update_button_visibility(False)
            messagebox.showerror('Error', f'Failed to load user data: {str(e)}')

    def update_user_info(self, user_data):
        title = user_data.get('title', '')
        name = f"{user_data.get('first_name', '')} {user_data.get('last_name', '')}".strip()
        user_info = f"Welcome,\n{title} {name}" if title and name else f"Welcome,\n{name or 'Guest'}"
        self.user_info_label.config(text=user_info)

    def update_button_visibility(self, is_operator):
        pass  # Implement role-based visibility if required

# StatrupClass
class StatrupClass:
    def __init__(self):
        self.window = tk.Tk()
        self.window.attributes('-fullscreen', True)
        self.window.geometry("1024x600")
        self.window.resizable(0, 0)
        self.window.configure(background='#64edb4')
        self.main_frame = Frame(self.window, bg='#64edb4')
        self.fliker_frame = Frame(self.window, bg='#64edb4')
        self.cff_fovea_frame = Frame(self.window, bg='#64edb4')
        self.cff_para_fovea_frame = Frame(self.window, bg='#64edb4')
        self.brkf1_frame = Frame(self.window, bg='#64edb4')
        self.brkf2_frame = Frame(self.window, bg='#64edb4')
        self.admin_frame = Frame(self.window, bg='#64edb4')
        currentPatientInfo.log_update("System_Started")
        globaladc.fan_on()
        self.mw = mainWindow(self.main_frame)
        self.fw = flikerWindow(self.fliker_frame)
        self.brkf_1 = BrkFovea_1(self.brkf1_frame)
        self.brkf_2 = BrkparaFovea(self.brkf2_frame)
        self.cff = CffFovea(self.cff_fovea_frame)
        self.cff_p = CffParaFovea(self.cff_para_fovea_frame)
        self.admin = Admin(self.admin_frame)
        self.login = LoginApp(self.window)
        self.login.callback = self.show_home_page  # Set callback to HomePage
        self.setup_buttons()

    def setup_buttons(self):
        self.admin_button = tk.Button(self.window, text="Admin", command=self.handle_admin, font=Font, width=10)
        self.start_button = tk.Button(self.window, text="Start", command=self.handle_start, font=Font, bg='Green', width=10)
        self.fliker_demo_button = tk.Button(self.window, text="Flicker Demo", command=self.handle_flicker_demo, font=Font, width=10)
        self.home_screen_button = tk.Button(self.window, text="Home", command=self.handle_home_screen, font=Font, width=10)
        self.save_button = tk.Button(self.brkf1_frame, text="Save", bg='#a0f291', command=self.handle_save, font=Font, width=10)
        self.save_button_2 = tk.Button(self.brkf2_frame, text="Save", bg='#a0f291', command=self.handle_save_2, font=Font, width=10)
        self.brkf_1.saveButton = self.save_button
        self.brkf_2.saveButton = self.save_button_2

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

    def hide_all(self):
        self.mw.hide()
        self.fw.hide()
        self.cff.hide()
        self.cff_p.hide()
        self.brkf_1.hide()
        self.brkf_2.hide()
        self.admin.hide()
        self.login.root.withdraw()
        if "HomePage" in pageDisctonary:
            pageDisctonary["HomePage"].hide_ui()
        self.hide_admin_button()
        self.hide_start_button()
        self.hide_fliker_button()
        self.hide_home_button()

    def show_login_screen(self):
        self.hide_all()
        self.login.load_ui()
        self.login.show_ui()
        self.login.root.deiconify()
        currentPatientInfo.log_update("Enter_to_Login_screen")

    def show_home_page(self):
        self.hide_all()
        if "HomePage" not in pageDisctonary:
            home_app = HomePage(self.window, self)
            pageDisctonary["HomePage"] = home_app
        pageDisctonary["HomePage"].show_ui()
        currentPatientInfo.log_update("Enter_to_Home_page")

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
        self.show_login_screen()
        self.window.mainloop()
        globaladc.buzzer_1()

if __name__ == "__main__":
    app = StatrupClass()
    app.main()