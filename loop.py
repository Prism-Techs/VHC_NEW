from PIL import Image, ImageTk
import time
from login import LoginApp  # Your login implementation
from Patient_checker import run_in_thread
import tkinter as tk

class LoadingScreen:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1024x600")
        self.root.overrideredirect(True)
        self.root.configure(bg='black')
        
        # Center the window
        self.center_window()
        # run_in_thread('patient_data','http://vhcbeta-api.prismtechs.in/patient/sync/','wifi_status.json')
        
        # Create canvas for logo
        self.canvas = tk.Canvas(root, width=1024, height=600, 
                              bg='black', highlightthickness=0)
        self.canvas.pack()
        
        # Load logo image
        try:
            self.logo = Image.open('loop.png')
            self.photo_image = None
            self.counter = 0
            
            # Start animation
            self.animate_logo()
            
        except Exception as e:
            print(f"Error loading logo: {e}")
            
    def center_window(self):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - 1024) // 2
        y = (screen_height - 600) // 2
        self.root.geometry(f"1024x600+{x}+{y}")

    def animate_logo(self):
        self.counter += 1
        
        if self.counter <= 40:  # Zoom in
            size = min(self.counter * 25, 600)
            resized_logo = self.logo.resize((size, size))
            if self.photo_image:
                self.canvas.delete("logo")
            self.photo_image = ImageTk.PhotoImage(resized_logo)
            
            # Center the image
            x = (1024 - size) // 2
            y = (600 - size) // 2
            self.canvas.create_image(x, y, anchor='nw', 
                                   image=self.photo_image, tags="logo")
            
            self.root.after(50, self.animate_logo)
            
        elif self.counter <= 50:  # Hold
            self.root.after(50, self.animate_logo)
            
        elif self.counter <= 60:  # Fade out
            opacity = 1 - (self.counter - 50) / 10
            self.root.attributes('-alpha', opacity)
            self.root.after(50, self.animate_logo)
            
        else:  # Animation complete
            self.show_writeup()

    def show_writeup(self):
        self.root.withdraw()  # Hide loading screen
        
        # Create write-up window
        self.writeup = tk.Toplevel()
        self.writeup.geometry("1024x600")
        self.writeup.overrideredirect(True)
        self.writeup.configure(bg='black')
        
        # Load and display write-up image
        try:
            writeup_img = Image.open('macular_densitometer_logo.png')
            writeup_img = writeup_img.resize((391, 331))
            self.writeup_photo = ImageTk.PhotoImage(writeup_img)
            
            img_label = tk.Label(self.writeup, image=self.writeup_photo, bg='black')
            img_label.place(x=50, y=110)
            
            # Add text
            text_label = tk.Label(
                self.writeup,
                text="Macular Densitometer is the only gold standard pre-clinical & clinical stage psycho-physical subjective (test) screening device - globally, for measuring Macular Pigment Optical Density (MPOD), using HFP (Heterochromatic Flicker Photometry Technology)",
                font=('Arial', 15),
                bg='black',
                fg='white',
                wraplength=481,
                justify='left'
            )
            text_label.place(x=440, y=130)
            
            # Bind click event to show login
            self.writeup.bind('<Button-1>', self.show_login)
            
        except Exception as e:
            print(f"Error loading writeup image: {e}")
            self.show_login(None)

    def show_login(self, event):
        self.writeup.withdraw()  # Hide write-up screen
        
        # Create login window
        login_window = tk.Toplevel()
        login_app = LoginApp(login_window)
        
        # Optional: handle login window close
        login_window.protocol("WM_DELETE_WINDOW", 
                            lambda: self.on_login_close(login_window))

    def on_login_close(self, login_window):
        login_window.destroy()
        self.root.destroy()

def main():
    root = tk.Tk()
    app = LoadingScreen(root)
    root.mainloop()

if __name__ == "__main__":
    main()