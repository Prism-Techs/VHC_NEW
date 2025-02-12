
import tkinter as tk
from tkinter import ttk, messagebox
from header import HeaderComponent
import json
import os
from datetime import datetime
from PIL import Image, ImageTk
from Keyboard import KeyBoard

class PatientRegistrationForm:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1024x600")
        self.root.configure(bg='black')
        # self.root.overrideredirect(True)
        
        self.kb = KeyBoard()
        
        # Variables for radio buttons
        self.gender_var = tk.StringVar(value="Male")
        self.alcohol_var = tk.StringVar(value="No")
        self.smoking_var = tk.StringVar(value="No")
        self.food_var = tk.StringVar(value="Veg")
        self.eye_side_var = tk.StringVar(value="R")
        self.bp_var = tk.StringVar(value="No")
        self.diabetes_var = tk.StringVar(value="No")
        
        self.setup_ui()

    def setup_ui(self):
        # Header
        self.header = HeaderComponent(self.root, "Patient-Registration")
        
        # Main Container
        self.main_frame = tk.Frame(self.root, bg='black')
        self.main_frame.place(x=20, y=120, width=981, height=460)
        
        # Create form fields with labels
        self.create_text_field("1st Name", 0, 20, "first name")
        self.create_text_field("Mid. Name", 344, 20, "Middle Name")
        self.create_text_field("Surname", 670, 20, "Surname")
        self.create_text_field("DOB", 0, 80, "Date of Birth")
        self.create_text_field("Aadhaar", 346, 80, "Aadhaar No")
        self.create_text_field("Mobile", 676, 80, "91XXXXXXXXXX")
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
            text="SUBMIT",
            font=('Arial', 24, 'bold'),
            bg='#1f2836',
            fg='white',
            bd=1,
            command=self.save_patient_data
        )
        self.submit_btn.place(x=410, y=390, width=161, height=51)
        
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

    def on_entry_focus_in(self, entry, placeholder):
        if entry.get() == placeholder:
            entry.delete(0, tk.END)
            entry.config(fg='white')
        self.kb.createAlphaKey(self.root, entry)

    def on_entry_focus_out(self, entry, placeholder):
        if entry.get() == '':
            entry.insert(0, placeholder)
            entry.config(fg='#94a3b8')

    def on_button_hover(self, event, button):
        button.configure(
            bg='#42A5F5',
            fg='white'
        )

    def on_button_leave(self, event, button):
        button.configure(
            bg='#1f2836',
            fg='white'
        )

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
                    "handler_id": 0
                }

                # Helper method to safely get entry values


                # Get current user data
                current_login_usr = os.path.join(os.path.dirname(os.path.realpath(__file__)), 
                                            "user_data", "latest_user.json")
                with open(current_login_usr, 'r') as f:
                    user_data = json.load(f)

                patient_data['handler_id'] = user_data['user_id']

                # Save patient data
                filename = f"patient_{patient_data['first_name']}.json"
                filepath = os.path.join(os.path.dirname(os.path.realpath(__file__)), 
                                    "patient_data", filename)

                os.makedirs(os.path.dirname(filepath), exist_ok=True)

                with open(filepath, 'w') as f:
                    json.dump(patient_data, f, indent=4)

                messagebox.showinfo("Success", "Patient data saved successfully!")
                self.root.withdraw()  # Hide current window
                
            except Exception as e:
                messagebox.showerror("Error", f"Error saving patient data: {str(e)}")




def main():
    root = tk.Tk()
    app = PatientRegistrationForm(root)
    root.mainloop()

if __name__ == "__main__":
    main()
