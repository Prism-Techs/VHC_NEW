import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import json
import os
from header import HeaderComponent
from Startupclass import StatrupClass

class HomePage:
    def __init__(self, root, startup_instance):
        self.root = root
        self.startup = startup_instance  # Reference to StatrupClass instance
        self.time_label = None
        self.date_label = None
        self.user_info_label = None
        self.buttons = []

        # Optimized constants
        self.colors = {
            'bg_black': 'black',
            'fg_white': 'white',
            'button_normal': '#101826',
            'button_hover': '#2196F3',
            'button_hover_fg': '#64B5F6'
        }
        self.fonts = {
            'welcome': ('Helvetica Neue', 14, 'bold'),
            'datetime': ('Helvetica Neue', 12),
            'button': ('Arial', 20, 'bold')
        }
        self.time_update_interval = 10000  # 10 seconds

        # Setup window
        self.root.geometry("1024x600")
        self.root.resizable(False, False)
        self.root.configure(bg=self.colors['bg_black'])
        self.root.overrideredirect(True)
        self.root.update_idletasks()

        # Initialize UI
        self.setup_ui()

    def __del__(self):
        """Cleanup Tkinter resources"""
        for button in self.buttons:
            button.destroy()
        self.time_label.destroy()
        self.date_label.destroy()
        self.user_info_label.destroy()
        self.header.destroy()

    def setup_ui(self):
        # Header (assuming it handles WiFi without image for now)
        self.header = HeaderComponent(self.root, "                                                    Home Page")
        self.header.set_wifi_callback(self.switch_to_wifi)

        # Welcome Label
        self.user_info_label = tk.Label(
            self.root, text="Welcome", font=self.fonts['welcome'], fg=self.colors['fg_white'],
            bg=self.colors['bg_black'], anchor='w'
        )
        self.user_info_label.place(x=20, y=150, width=280, height=40)

        # Buttons
        button_configs = [
            ("Create User", 382, 150, self.create_user),
            ("View Reports", 382, 250, self.view_reports),
            ("Test Mode", 382, 350, self.test_mode),
            ("Logout", 382, 450, self.logout)
        ]
        for text, x, y, command in button_configs:
            button = tk.Button(
                self.root, text=text, command=command, font=self.fonts['button'],
                bg=self.colors['button_normal'], fg=self.colors['fg_white'], bd=1,
                relief='solid', width=15, height=1
            )
            button.place(x=x, y=y)
            button.bind('<Enter>', lambda e, b=button: b.config(bg=self.colors['button_hover'], fg=self.colors['button_hover_fg'], bd=2))
            button.bind('<Leave>', lambda e, b=button: b.config(bg=self.colors['button_normal'], fg=self.colors['fg_white'], bd=1))
            self.buttons.append(button)

        # Time and Date Labels
        self.time_label = tk.Label(self.root, font=self.fonts['datetime'], fg=self.colors['fg_white'], bg=self.colors['bg_black'])
        self.time_label.place(x=900, y=560)
        self.date_label = tk.Label(self.root, font=self.fonts['datetime'], fg=self.colors['fg_white'], bg=self.colors['bg_black'])
        self.date_label.place(x=900, y=580)

        # Initial datetime update
        self.update_datetime()

        # Check user role
        self.check_user_role()

    def update_datetime(self):
        current = datetime.now()
        self.time_label.config(text=current.strftime('%H:%M'))
        self.date_label.config(text=current.strftime('%d-%m-%Y'))
        self.root.after(self.time_update_interval, self.update_datetime)

    def switch_to_wifi(self):
        """Switch to WifiSettings frame instead of opening a new window"""
        if "WifiSettings" not in pageDisctonary:
            wifi_frame = tk.Frame(self.root, bg='#64edb4')
            pageDisctonary["WifiSettings"] = WifiSettings(wifi_frame, self.startup)
            pageDisctonary["WifiSettings"].Load()
        self.startup.HideStartButton()
        self.startup.HideAdminButton()
        self.startup.HideFlikerButton()
        self.startup.ShowHomeButton()
        pageDisctonary["MainScreen"].hide()
        pageDisctonary["WifiSettings"].show()

    def create_user(self):
        messagebox.showinfo("Action", "Create User functionality to be implemented")
        print("Create user clicked")

    def view_reports(self):
        messagebox.showinfo("Action", "View Reports functionality to be implemented")
        print("View reports clicked")

    def test_mode(self):
        self.root.withdraw()
        st = self.startup
        st.main()
        self.root.deiconify()

    def logout(self):
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.root.destroy()
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

def main():
    try:
        os.nice(10)
    except AttributeError:
        pass

    root = tk.Tk()
    root.update_idletasks()
    startup = StatrupClass()
    app = HomePage(root, startup)
    pageDisctonary["MainScreen"] = app
    root.mainloop()

if __name__ == "__main__":
    main()