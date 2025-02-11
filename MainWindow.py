import datetime
import imp
import time
import tkinter as tk
from tkinter import Frame, ttk
from Keyboard import KeyBoard
from FlikerScreen import flikerWindow
from CFF_FOVEA import CffFovea
from globalvar import pageDisctonary
from globalvar import currentPatientInfo
from Splash import Splash
from globalvar import globaladc
import tkinter.font as tkfont
from header import HeaderComponent
import os,json
from tkinter import messagebox
from datetime import datetime
import pytz


FONT_SIZE = 10
Font = ("Arial",30)
# HIGHT = 1
# WIDTH = 10
Font2 = ("Arial",20)
Font3 = ("Arial",30)

class mainWindow:

    def __init__(self, frame):
        self.frame = frame
        self.frame.configure(bg='black')
        self.selectedGen = "M"
        self.selectedEye = "R" 



        self.kb = KeyBoard()
        
        # Variables for radio buttons
        self.gender_var = tk.StringVar(value="Male")
        self.alcohol_var = tk.StringVar(value="No")
        self.smoking_var = tk.StringVar(value="No")
        self.food_var = tk.StringVar(value="Veg")
        self.eye_side_var = tk.StringVar(value="R")
        self.bp_var = tk.StringVar(value="No")
        self.diabetes_var = tk.StringVar(value="No")


    def save_patient_data(self):
        try:
            # Get values from stored entry widgets using the correct attribute names
            patient_data = {
                "first_name": self.get_entry_value("1st", "_name_entry"),
                "middle_name": self.get_entry_value("mid", "_name_entry"),
                "surname": self.get_entry_value("surname", "_entry"),
                "dob": self.get_entry_value("dob", "_entry"),
                "aadhaar": self.get_entry_value("aadhaar", "_entry"),
                "mobile": self.get_entry_value("mobile", "_entry"),
                "nationality": self.get_entry_value("nationality", "_entry"),
                "gender": self.gender_var.get(),
                "alcohol": self.alcohol_var.get(),
                "smoking": self.smoking_var.get(),
                "food_habit": self.food_var.get(),
                "bp": {
                    "has_bp": self.bp_var.get(),
                    "value": self.get_entry_value("blood_pressure", "_entry")
                },
                "diabetes": {
                    "has_diabetes": self.diabetes_var.get(),
                    "value": self.get_entry_value("diabetes", "_entry")
                },
                "eye_side": self.eye_side_var.get(),
                "is_sync": False,
                "handler_id": 0,
                "CFF_F":'',
                "CFF_P":'',
                "f_mpod":'',
                "f-sd":'',
            }

            # Helper method to safely get entry values


            # Get current user data
            current_login_usr = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                                        "user_data", "latest_user.json")
            with open(current_login_usr, 'r') as f:
                user_data = json.load(f)

            patient_data['handler_id'] = user_data['user_id']

            # Save patient data
            filename = f"patient_latest.json"
            filepath = os.path.join(os.path.dirname(os.path.realpath(__file__)), 
                                "patient_data", filename)
            

            filename = f"patient_{self.get_entry_value('1st', '_name_entry')}.json"
            filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                                "patient_data", filename)

            os.makedirs(os.path.dirname(filepath), exist_ok=True)

            with open(filepath, 'w') as f:
                json.dump(patient_data, f, indent=4)

            messagebox.showinfo("Success", "Patient data saved successfully!")
            # StatrupClass.handleStart()
            
            
        except Exception as e:
            messagebox.showerror("Error", f"Error saving patient data: {str(e)}")


    def get_entry_value(self, prefix, suffix):
                    attribute_name = f"{prefix}{suffix}"
                    entry_widget = getattr(self, attribute_name, None)
                    if entry_widget is None:
                        return ""  # Return empty string if widget not found
                    value = entry_widget.get()
                    # Remove placeholder text if present
                    if value in ["first name", "Middle Name", "Surname", "Date of Birth", 
                            "Aadhaar No", "+91XXXXXXXXXX", "80/120", "97"]:
                        return ""
                    return value

    def on_button_leave(self, event, button):
        button.configure(
            bg='#1f2836',
            fg='white'
        )

    def on_button_hover(self, event, button):
        button.configure(
            bg='#42A5F5',
            fg='white'
        )

    def on_entry_focus_in(self, entry, placeholder):
        if entry.get() == placeholder:
            entry.delete(0, tk.END)
            entry.config(fg='white')
        
        # Create keyboard on focus in
        self.kb.createAlphaKey(self.frame, entry)

    def on_entry_focus_out(self, entry, placeholder):
        # Get the currently focused widget
        focused = self.frame.focus_get()
        
        # Only cleanup keyboard if focus is not on the keyboard window or its children
        if not (self.kb.current_window and 
                focused and 
                (focused == self.kb.current_window or 
                 focused.winfo_toplevel() == self.kb.current_window)):
            
            if entry.get() == '':
                entry.insert(0, placeholder)
                entry.config(fg='#94a3b8')
            
            # Add longer delay for cleanup
            self.frame.after(200, self.check_focus_and_cleanup, entry)


    def cleanup_keyboard(self):
            """Remove existing keyboard if it exists"""
            if hasattr(self, 'kb') and self.kb is not None:
                try:
                    # Find and destroy the keyboard frame
                    for widget in self.frame.winfo_children():
                        if isinstance(widget, tk.Frame) and widget.winfo_name().startswith('keyboard'):
                            widget.destroy()
                    self.kb = None
                except:
                    pass

    def check_focus_and_cleanup(self, original_entry):
        """Check if focus has moved away from entry and keyboard before cleanup"""
        focused = self.frame.focus_get()
        
        # Only cleanup if focus is not on original entry or keyboard
        if (focused != original_entry and 
            not (self.kb.current_window and 
                 focused and 
                 (focused == self.kb.current_window or 
                  focused.winfo_toplevel() == self.kb.current_window))):
            # self.kb.cleanup_keyboard()
            pass

    def setup_ui(self):
        # Header
        self.header = HeaderComponent(self.frame, "Macular Densitometer                                                       Patient-Registration")
        
        # Main Container
        self.main_frame = tk.Frame(self.frame, bg='black')
        self.main_frame.place(x=20, y=120, width=981, height=460)
        
        # Create form fields with labels
        self.create_text_field("1st Name", 0, 20, "first name")
        self.create_text_field("Mid. Name", 344, 20, "Middle Name")
        self.create_text_field("Surname", 670, 20, "Surname")
        self.create_text_field("DOB", 0, 80, "Date of Birth")
        self.create_text_field("Aadhaar", 346, 80, "Aadhaar No")
        self.create_text_field("Mobile", 676, 80, "+91XXXXXXXXXX")
        self.create_text_field("Nationality", 450, 320, "Enter Nationality")
        
        # Radio button groups
        self.create_radio_group("Gender", 0, 140, self.gender_var, [("Male", "Male"), ("Female", "Female")])
        self.create_radio_group("Eye Side", 450, 140, self.eye_side_var, [("R", "R"), ("L", "L")])
        self.create_radio_group("Alcohol", 0, 200, self.alcohol_var, [("Yes", "Yes"), ("No", "No")])
        self.create_radio_group("Smoking", 0, 260, self.smoking_var, [("Yes", "Yes"), ("No", "No")])
        self.create_radio_group("Food Habit", 0, 320, self.food_var, [("Veg", "Veg"), ("NON-Veg", "NON-Veg")])
        
        # BP and Diabetes section
        self.create_medical_field("Blood Pressure", 450, 200, self.bp_var, "80/120")
        self.create_medical_field("Diabetes", 450, 260, self.diabetes_var, "97")
        
        # Submit Button
        self.submit_btn = tk.Button(
            self.main_frame,
            text="SAVE",
            font=('Arial', 24, 'bold'),
            bg='#1f2836',
            fg='white',
            bd=1,
            command=self.save_patient_data
        )
        self.submit_btn.place(x=650, y=390, width=161, height=51)
        
        # Bind hover effects
        self.submit_btn.bind('<Enter>', lambda e: self.on_button_hover(e, self.submit_btn))
        self.submit_btn.bind('<Leave>', lambda e: self.on_button_leave(e, self.submit_btn))

    def create_text_field(self, label_text, x, y, placeholder):
            # Label
            label = tk.Label(
                self.main_frame,
                text=label_text,
                font=('Helvetica Neue', 16),
                bg='black',
                fg='white'
            )
            label.place(x=x, y=y)
            
            # Text Entry
            entry = tk.Entry(
                self.main_frame,
                font=('Helvetica', 14),
                bg='#334155',
                fg='#94a3b8',
                insertbackground='white'
            )
            entry.place(x=x+140, y=y, width=190, height=31)
            entry.insert(0, placeholder)
            
            # Update bindings to use instance methods
            entry.bind('<FocusIn>', lambda e: self.on_entry_focus_in(entry, placeholder))
            entry.bind('<FocusOut>', lambda e: self.on_entry_focus_out(entry, placeholder))
            
            # Store entry widget reference
            setattr(self, f"{label_text.lower().replace(' ', '_')}_entry", entry)


    def create_radio_group(self, label_text, x, y, variable, options):
            # Label
            label = tk.Label(
                self.main_frame,
                text=label_text,
                font=('Helvetica Neue', 16),
                bg='black',
                fg='white'
            )
            label.place(x=x, y=y)
            
            # Radio buttons
            for i, (value, text) in enumerate(options):
                rb = tk.Radiobutton(
                    self.main_frame,
                    text=text,
                    variable=variable,
                    value=value,
                    font=('Helvetica Neue', 14),
                    bg='black',
                    fg='white',
                    selectcolor='black',  # Changed from '#42A5F5' to 'black'
                    activebackground='black',
                    activeforeground='white',
                    highlightthickness=0,  # Remove highlight border
                    highlightbackground='black',
                    highlightcolor='black'
                )
                rb.place(x=x+140+(i*120), y=y)


    def create_medical_field(self, label_text, x, y, variable, placeholder):
            # Label
            label = tk.Label(
                self.main_frame,
                text=label_text,
                font=('Helvetica Neue', 16),
                bg='black',
                fg='white'
            )
            label.place(x=x, y=y)
            
            # Radio buttons
            tk.Radiobutton(
                self.main_frame,
                text="Yes",
                variable=variable,
                value="Yes",
                font=('Helvetica Neue', 14),
                bg='black',
                fg='white',
                selectcolor='black',  # Changed from '#42A5F5' to 'black'
                activebackground='black',
                activeforeground='white',
                highlightthickness=0,
                highlightbackground='black',
                highlightcolor='black'
            ).place(x=x+210, y=y)
            
            tk.Radiobutton(
                self.main_frame,
                text="No",
                variable=variable,
                value="No",
                font=('Helvetica Neue', 14),
                bg='black',
                fg='white',
                selectcolor='black',  # Changed from '#42A5F5' to 'black'
                activebackground='black',
                activeforeground='white',
                highlightthickness=0,
                highlightbackground='black',
                highlightcolor='black'
            ).place(x=x+300, y=y)

    def Load(self):
        kb = KeyBoard()
        a=50
        # time label
        #x=datetime.datetime.now () 
        # self.timelabel = tk.Label (self.frame,font=Font)
        # self.updateDateTime()
        # # self.timelabel.place(x=550, y=10)
        
        # #Name amd name text
        # self.Namelabel = tk.Label (self.frame,font=Font, text="Name")
        # self.Namelabel.place (x=a+25, y=80)        
        # self.NameText = tk.Entry (self.frame,
        #                      font=Font,
        #                      justify="left")
        # self.NameText.bind ("<FocusIn>",
        #                lambda event: kb.createAlphaKey(self.frame,self.NameText))
        # #self.NameText.bind ("<FocusOut>",
        # #                lambda event:nameTextFocusOut(NameText))               
        # self.NameText.place (x=a+175,y=80)        
        # self.Agelabel = tk.Label (self.frame,text="Age",font=Font)
        # self.Agelabel.place (x=a+25, y=200)
        # self.AgeText = tk.Entry (self.frame,font=Font, width=3)
                           
        # self.AgeText.bind ("<FocusIn>", lambda event: kb.createNumaKey(self.frame,self.AgeText))
        # self.AgeText.place (x=a+125, y=200)
      
      
        # self.Genderlabel = tk.Label (self.frame, text="Gender",font=Font)
        # self.Genderlabel.place (x=a+225, y=200)

        # self.GenderSel = tk.Button (self.frame, text = 'M', width=4, font=Font2, bg="#90b2f5", command=self.genderSelected)
        # self.GenderSel.place (x=a+375, y=200)
        
      
        # self.Eyelabel = tk.Label (self.frame, text="Eye :",font=Font)
        # self.Eyelabel.place (x=a+475, y=200)

        # self.EyeSel = tk.Button (self.frame, text = 'R', width=4, font=Font2, bg="#87aaf5", command=self.eyeSelected)
        # self.EyeSel.place (x=a+555, y=200) 
        # globaladc.skip_rset()
        # globaladc.main_Prepair() 

        self.setup_ui()

         
        def onfw():
            pageDisctonary['MainScreen'].hide()
            pageDisctonary['CffFovea'].show()  #'CffFovea'


        def onbw():
            pageDisctonary['MainScreen'].hide()
            pageDisctonary['BrkparaFovea'].show()

        fwButton = tk.Button (self.frame,
                                 text=">>", font=Font2,
                                 command=onfw, bg='#a0f291',
                                 width=10)
       
        bwButton = tk.Button (self.frame,
                                 text="<<", font=Font2,
                                 command=onbw, bg='#a0f291',
                                 width=10)
 
#         fwButton.place (x=620,y=500)
#         bwButton.place (x=420, y=500)
               #Button start the test
        
        

    def handleStart():
            CffFovea.Open()

    def wifi_page(self):
        globaladc.buzzer_3()

    def updateDateTime(self):
       raw_dt = datetime.datetime.now()
       #date_now = raw_dt.strftime("%d %b %y")
      # time_now = raw_dt.strftime("%d %b %Y %H : %M : %S %p")
       time_now = raw_dt.strftime("%d/%m/%Y %I:%M:%S %p")
      # self.timelabel.config(text = date_now)
       self.timelabel.config(text = time_now)
       self.timelabel.after(1000,self.updateDateTime)
       
    def genderSelected(self):
        if(self.GenderSel['text'] == 'M'):
            self.GenderSel['text'] = 'F'
            self.GenderSel['bg']="#f29be4"    
        else :
            self.GenderSel['text'] = 'M'
            self.GenderSel['bg']="#90b2f5"    
  
        self.selectedGen =self.GenderSel['text']
               
   
    def eyeSelected(self, value):
        """Handle eye selection"""
        self.eye_side_var.set(value)  # Update the eye side variable
        currentPatientInfo.eye = value  # Update the current patient info
        
        # Update visual feedback in radio buttons
        for rb in self.main_frame.winfo_children():
            if isinstance(rb, tk.Radiobutton) and rb['value'] in ['R', 'L']:
                if rb['value'] == value:
                    rb.configure(bg='#87aaf5')  # Blue for selected
                else:
                    rb.configure(bg='black')  # Black for unselected

    def show(self):        
        self.frame.place(width=1024,height=600)
        # time.sleep(1)
        globaladc.main_Prepair() # run this while loading main Screen
    
    def hide(self):
        self.frame.place_forget()

    def getName():
        return "MainScreen"    
    
    def age_calculator(self):
        dob_str = self.get_entry_value('dob', '_entry')  # Assuming this returns DOB as a string (e.g., "1998-06-15")

        if not dob_str:
             messagebox.showerror("Input error","Please enter a vali Date of Birth")
             return
        
        try:
                dob = datetime.strptime(dob_str,"%d/%m/%y")


                # Get current time in Indian time zone (IST)
                indian_timezone = pytz.timezone("Asia/Kolkata")
                today = datetime.now(indian_timezone).date()  # Get today's date in IST

                # Calculate age
                age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

                return age

    
        except ValueError:
            messagebox.showerror("Format Error", "Please enter DOB in dd/mm/yy format")


    def loadValues(self):
        currentPatientInfo.Name = f"{self.get_entry_value('1st', '_name_entry')} {self.get_entry_value('mid', '_name_entry')} {self.get_entry_value('surname', '_entry')}"
        currentPatientInfo.Age = self.age_calculator()  # Using DOB field for age
        currentPatientInfo.eye = self.eye_side_var.get()  # Get selected eye side (R/L)
        currentPatientInfo.Gender = "M" if self.gender_var.get() == "Male" else "F"  # Convert gender to M/F format
        
            # Get current date/time
        current_datetime = datetime.now().strftime("%d/%m/%Y %I:%M:%S %p")
        currentPatientInfo.date = current_datetime

    def ValidateUserInput(self):
        valid = True
        
        # Check required fields
        if not self.get_entry_value('1st', '_name_entry'): valid = False  # First name
        # if not self.get_entry_value('dob', '_entry'): valid = False      # DOB/Age
        if not self.eye_side_var.get(): valid = False                    # Eye side
        if not self.gender_var.get(): valid = False                      # Gender
        
        if valid:
            self.loadValues()
        
        return valid
        
        
