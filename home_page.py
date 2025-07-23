import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import json
import os
from header import HeaderComponent
from globalvar import pageDisctonary

class HomePage:
    def __init__(self, frame, startup_instance):
        self.frame = frame  # Changed from root to frame for consistency
        self.startup = startup_instance
        self.buttons = []
        self.colors = {'bg_black': 'black', 'fg_white': 'white', 'button_normal': '#101826', 'button_hover': '#2196F3', 'button_hover_fg': '#64B5F6'}
        self.fonts = {'welcome': ('Helvetica Neue', 14, 'bold'), 'datetime': ('Helvetica Neue', 12), 'button': ('Arial', 20, 'bold')}
        self.time_update_interval = 1000  # Changed to 1000ms (1s) for smoother updates
        self.frame.configure(bg=self.colors['bg_black'])

    def Load(self):  # Renamed from load_ui to match convention
        self.header = HeaderComponent(self.frame, "Macular Densitometer                                                     Home Page")
        self.user_info_label = tk.Label(self.frame, text="Welcome", font=self.fonts['welcome'], fg=self.colors['fg_white'],
                                      bg=self.colors['bg_black'], anchor='w')
        self.button_configs = [
            ("Create User", self.create_user),
            ("View Reports", self.view_reports),
            ("Test Mode", self.test_mode),
            ("Logout", self.logout)
        ]
        self.buttons = []
        for text, command in self.button_configs:
            button = tk.Button(self.frame, text=text, command=command, font=self.fonts['button'], bg=self.colors['button_normal'],
                             fg=self.colors['fg_white'], bd=1, relief='solid', width=15, height=1)
            self.buttons.append(button)
        # self.time_label = tk.Label(self.frame, font=self.fonts['datetime'], fg=self.colors['fg_white'], bg=self.colors['bg_black'])
        # self.date_label = tk.Label(self.frame, font=self.fonts['datetime'], fg=self.colors['fg_white'], bg=self.colors['bg_black'])

    def show(self):  # Renamed from show_ui to match convention
        self.frame.place(width=1024, height=600)  # Full screen placement
        self.header.set_wifi_callback(self.switch_to_wifi)
        self.user_info_label.place(x=20, y=150, width=280, height=40)
        y_positions = [150, 250, 350, 450]
        for i, button in enumerate(self.buttons):
            button.place(x=382, y=y_positions[i])
            button.bind('<Enter>', lambda e, b=button: b.config(bg=self.colors['button_hover'], fg=self.colors['button_hover_fg'], bd=2))
            button.bind('<Leave>', lambda e, b=button: b.config(bg=self.colors['button_normal'], fg=self.colors['fg_white'], bd=1))
        # self.time_label.place(x=900, y=560)
        # self.date_label.place(x=900, y=580)
        self.update_datetime()
        self.check_user_role()

    def hide(self):  # Renamed from hide_ui to match convention
        self.frame.place_forget()

    def update_datetime(self):
        current = datetime.now()
        # self.time_label.config(text=current.strftime('%H:%M'))
        # self.date_label.config(text=current.strftime('%d-%m-%Y'))
        self.frame.after(self.time_update_interval, self.update_datetime)

    def switch_to_wifi(self):
        # Placeholder for WiFi settings (uncomment and implement if needed)
        # if "WifiSettings" not in pageDisctonary:
        #     wifi_frame = tk.Frame(self.frame.master, bg='#64edb4')
        #     pageDisctonary["WifiSettings"] = WifiSettings(wifi_frame, self.startup)
        #     pageDisctonary["WifiSettings"].Load()
        # self.startup.hide_all()
        # self.startup.show_home_button()
        # pageDisctonary["WifiSettings"].show()
        print("Switching to WiFi settings")

    def create_user(self):
        messagebox.showinfo("Action", "Create User functionality to be implemented")
        print("Create user clicked")

    def view_reports(self):
        messagebox.showinfo("Action", "View Reports functionality to be implemented")
        print("View reports clicked")

    def test_mode(self):
        self.hide()
        self.startup.ShowMainScreen()  # Changed to ShowMainScreen for consistency with flow

    def logout(self):
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.hide()
            self.startup.ShowLoginScreen()  # Changed to ShowLoginScreen for consistency
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
        # Example: Hide "Create User" for non-operators
        if not is_operator:
            self.buttons[0].place_forget()  # Hide "Create User" button
        else:
            self.buttons[0].place(x=382, y=150)  # Show it back if operator