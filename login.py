import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import json
import os
from PIL import Image, ImageTk
from header import HeaderComponent
from database import DatabaseConnection
from Keyboard import KeyBoard

class LoginApp:
    def __init__(self, frame):
        self.root = frame
        self.root.configure(bg='black')
        self.kb = KeyBoard()
        
        # Initialize variables
        self.wifi_window = None
        self.password_visible = False

        # Create JSON directory
        self.json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "user_data")
        if not os.path.exists(self.json_path):
            os.makedirs(self.json_path)

        # Load and show UI
    

    def load_ui(self):
        """Create all UI components without placing them"""
        # Header component
        self.header = HeaderComponent(self.root, "                                                       Macular Densitometer")

        # Main content frame
        self.content_frame = tk.Frame(self.root,
                                    bg='#1f2836',
                                    highlightbackground='white',
                                    highlightthickness=1)

        # Username entry
        self.username = tk.Entry(self.content_frame,
                               font=('Helvetica', 18),
                               bg='#334155',
                               fg='#94a3b8',
                               insertbackground='white')
        self.username.insert(0, "Username")

        # Password entry
        self.password = tk.Entry(self.content_frame,
                               font=('Helvetica', 18),
                               bg='#334155',
                               fg='#94a3b8',
                               insertbackground='white',
                               show='*')
        self.password.insert(0, "Password")

        # Password toggle button
        self.toggle_btn = tk.Button(self.content_frame,
                                  text="Show",
                                  font=('Arial', 12),
                                  bg='#334155',
                                  fg='white',
                                  bd=0,
                                  highlightthickness=0,
                                  activebackground='#334155',
                                  activeforeground='#42A5F5',
                                  cursor="hand2",
                                  command=self.toggle_password)

        # Operation mode label
        self.mode_label = tk.Label(self.content_frame,
                                 text="Operation Mode",
                                 font=('Helvetica Neue', 18, 'bold'),
                                 bg='#1f2836',
                                 fg='white')

        # Radio buttons setup
        self.operation_mode = tk.StringVar(value="Clinic")
        self.radio_frame = tk.Frame(self.content_frame, bg='#1f2836')
        self.radio_buttons = {}
        radio_style = {
            'font': ('Helvetica Neue', 12, 'bold'),
            'fg': 'white',
            'selectcolor': '#42A5F5',
            'padx': 20,
            'variable': self.operation_mode,
            'height': 2,
            'width': 10,
            'indicatoron': 0
        }
        modes = [("Eye Camp", "Eye Camp"), ("Clinic", "Clinic"), ("Demo", "Demo")]
        for text, mode in modes:
            rb = tk.Radiobutton(self.radio_frame,
                              text=text,
                              value=mode,
                              bg='#1f2836',
                              activebackground='#1f2836',
                              **radio_style)
            self.radio_buttons[mode] = rb

        # Login button
        self.login_btn = tk.Button(self.content_frame,
                                 text="LOGIN",
                                 font=('Arial', 24, 'bold'),
                                 bg='#1f2836',
                                 fg='white',
                                 bd=1,
                                 relief='solid',
                                 command=self.handle_login)

        # Time and date labels
        self.time_label = tk.Label(self.root,
                                 font=('Helvetica Neue', 10),
                                 bg='black',
                                 fg='white')
        self.date_label = tk.Label(self.root,
                                 font=('Helvetica Neue', 10),
                                 bg='black',
                                 fg='white')

    def show_ui(self):
        """Place and configure all UI components"""
        # Place header and set callback
        self.header.set_wifi_callback(self.open_wifi_page)

        # Place content frame
        self.content_frame.place(x=200, y=115, width=624, height=430)

        # Place and bind username entry
        self.username.place(x=62, y=50, width=500, height=61)
        self.username.bind('<FocusIn>', lambda e: self.on_entry_click(self.username, "Username"))
        self.username.bind('<FocusOut>', lambda e: self.on_focus_out(self.username, "Username"))

        # Place and bind password entry
        self.password.place(x=62, y=140, width=500, height=61)
        self.password.bind('<FocusIn>', lambda e: self.on_entry_click(self.password, "Password"))
        self.password.bind('<FocusOut>', lambda e: self.on_focus_out(self.password, "Password"))

        # Place toggle button
        self.toggle_btn.place(x=520, y=150, width=40, height=40)

        # Place mode label
        self.mode_label.place(x=112, y=210, width=400, height=71)

        # Place and configure radio buttons
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

        # Place and bind login button
        self.login_btn.place(x=230, y=350, width=161, height=51)
        self.login_btn.bind('<Enter>', self.on_login_hover)
        self.login_btn.bind('<Leave>', self.on_login_leave)

        # Place time and date labels
        self.time_label.place(x=960, y=550)
        self.date_label.place(x=934, y=570)

        # Start time updates
        self.update_datetime()

    def update_radio_styles(self, *args):
        """Update radio button styles based on selection"""
        selected_value = self.operation_mode.get()
        for value, rb in self.radio_buttons.items():
            if value == selected_value:
                rb.configure(bg='#42A5F5', activebackground='#42A5F5', fg='white')
            else:
                rb.configure(bg='#1f2836', activebackground='#1f2836', fg='white')

    def on_login_hover(self, event):
        """Handle login button hover effect"""
        self.login_btn.configure(bg='#42A5F5', fg='white')

    def on_login_leave(self, event):
        """Handle login button hover leave effect"""
        self.login_btn.configure(bg='#1f2836', fg='white')

    def update_datetime(self):
        """Update time and date labels"""
        current_time = datetime.now().strftime('%H:%M')
        current_date = datetime.now().strftime('%d-%m-%Y')
        self.time_label.config(text=current_time)
        self.date_label.config(text=current_date)
        self.root.after(1000, self.update_datetime)

    def on_entry_click(self, entry, default_text):
        """Handle entry field focus in"""
        current_text = entry.get().strip()
        if current_text == default_text:
            entry.delete(0, tk.END)
            entry.configure(fg='white')
            if entry == self.password and current_text != "Password":
                entry.configure(show='*')
        self.kb.createAlphaKey(self.root, entry)

    def on_focus_out(self, entry, default_text):
        """Handle entry field focus out"""
        current_text = entry.get().strip()
        if current_text == '':
            entry.delete(0, tk.END)
            entry.insert(0, default_text)
            entry.configure(fg='#94a3b8')
            if entry == self.password:
                entry.configure(show='')

    def toggle_password(self):
        """Toggle password visibility"""
        self.password_visible = not self.password_visible
        if self.password_visible:
            self.password.configure(show='')
            self.toggle_btn.configure(text='Hide', fg='#42A5F5')
        else:
            self.password.configure(show='*')
            self.toggle_btn.configure(text='Show', fg='white')

    def open_wifi_page(self):
        """Open WiFi settings window (placeholder)"""
        print("Opening WiFi page")

    def generate_user_json(self, user_data, operation_mode):
        """Generate JSON file with user information"""
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
        """Handle login button click"""
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
                # Uncomment and adjust as needed for home page transition
                # startup_instance = StatrupClass()
                # home_window = tk.Toplevel()
                # home_app = HomePage(home_window, startup_instance)
                # pageDisctonary["MainScreen"] = home_app
                # home_window.protocol("WM_DELETE_WINDOW", lambda: self.on_home_close(home_window, startup_instance))
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

    def on_home_close(self, home_window, startup_instance):
        """Handle home window closing"""
        home_window.destroy()
        self.root.deiconify()
        startup_instance.window.destroy()

