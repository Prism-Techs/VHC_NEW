import tkinter as tk
import time
import threading

class AnimatedWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("1024x600")
        self.root.title("Machine Initialization")
        
        # Set dark background
        self.root.configure(bg='#1a1a1a')
        
        # Create canvas for dot animation
        self.canvas = tk.Canvas(
            self.root,
            width=1024,
            height=600,
            bg='#1a1a1a',
            highlightthickness=0
        )
        self.canvas.pack(fill='both', expand=True)
        
        # Initialize dot properties
        self.text_id = None
        self.current_dots = "."
        self.max_dots = 4
        self.dot_count = 1
        self.animation_running = True
        
        # Start animation in a separate thread
        self.animation_thread = threading.Thread(target=self.animate_dots)
        self.animation_thread.daemon = True
        self.animation_thread.start()
        
    def animate_dots(self):
        """Animate dots appearing and resetting"""
        while self.animation_running:
            time.sleep(0.5)  # Delay between each dot state
            
            # Update dot count and text
            self.dot_count = (self.dot_count % self.max_dots) + 1
            self.current_dots = "." * self.dot_count
            
            # Update dots on canvas (must be done in main thread)
            self.root.after(0, self.update_dots)
    
    def update_dots(self):
        """Update the dots display on canvas"""
        # Clear previous text
        if self.text_id:
            self.canvas.delete(self.text_id)
        
        # Calculate center position
        x = self.canvas.winfo_width() // 2
        y = self.canvas.winfo_height() // 2
        
        # Draw new dots
        display_text = "Machine Initialization" + self.current_dots
        self.text_id = self.canvas.create_text(
            x, y,
            text=display_text,
            font=('Courier', 36, 'bold'),
            fill='#00ff00',  # Matrix-style green text
            anchor='center'
        )
    
    def run(self):
        """Start the main event loop"""
        self.root.mainloop()
        self.animation_running = False

if __name__ == "__main__":
    app = AnimatedWindow()
    app.run()