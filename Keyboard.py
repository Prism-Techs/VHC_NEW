import tkinter as tk
from globalvar import globaladc

class KeyBoard:
    def __init__(self):
        self.shift_active = False
        self._drag_data = {"x": 0, "y": 0}  # For dragging
        self.current_window = None  # Track current keyboard window
        self.current_entry = None  # Track current entry

    def cleanup_keyboard(self):
        if self.current_window and self.current_window.winfo_exists():
            try:
                self.current_window.destroy()
                self.current_window = None
                self.current_entry = None
            except tk.TclError:
                self.current_window = None
                self.current_entry = None

    def on_drag_start(self, event, window):
        """Begin drag of the window"""
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y

    def on_drag_motion(self, event, window):
        """Handle dragging of the window"""
        if window.winfo_exists():  # Check if window still exists
            delta_x = event.x - self._drag_data["x"]
            delta_y = event.y - self._drag_data["y"]
            x = window.winfo_x() + delta_x
            y = window.winfo_y() + delta_y
            window.geometry(f"+{x}+{y}")
            window.lift()  # Keep window on top while dragging

    def select(self, entry, window, mainwindow, value, ucase=None):
        """Handle key selection and input"""
        if not window.winfo_exists():  # Check if window still exists
            return

        uppercase = ucase

        if value == "Space":
            value = ' '
        elif value == 'Enter':
            value = ''
            globaladc.get_print("enter pressed")
            mainwindow.focus_force()
            self.cleanup_keyboard()
            return
        elif value == 'Tab':
            value = '\t'

        if value == "Back" or value == '<-':
            if isinstance(entry, tk.Entry):
                if len(entry.get()) > 0:
                    entry.delete(len(entry.get())-1, 'end')
            else:
                entry.delete('end - 2c', 'end')

        elif value == 'Shift':
            self.shift_active = not self.shift_active
            for widget in window.winfo_children():
                if isinstance(widget, tk.Frame):
                    for btn in widget.winfo_children():
                        if isinstance(btn, tk.Button) and btn['text'] not in ['Space', 'Enter', 'Back', 'Shift', '<-']:
                            btn['text'] = btn['text'].upper() if self.shift_active else btn['text'].lower()

        elif value not in ('Caps Lock', 'Shift'):
            if self.shift_active:
                value = value.upper()
            entry.insert('end', value)
            entry.focus_set()  # Keep focus on the entry

        globaladc.buzzer_1()
        window.lift()  # Keep keyboard on top after each action

    def createAlphaKey(self, root, entry, number=False):
        """Create alphabetic keyboard"""
        # Don't recreate keyboard if it's already showing for this entry
        if self.current_window and self.current_window.winfo_exists() and self.current_entry == entry:
            self.current_window.lift()
            return self.current_window

        self.cleanup_keyboard()
        self.current_entry = entry

        alphabets = [
            ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '@'],
            ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '#'],
            ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', '/', '*'],
            ['Shift ^', 'z', 'x', 'c', 'v', 'b', 'n', 'm', '!', 'Back'],
            ['Space', 'Enter']
        ]

        window = tk.Toplevel(root)
        window.attributes('-topmost', True)  # Make window stay on top
        self.current_window = window

        x = root.winfo_x()
        y = root.winfo_y()

        # Set initial size and allow resizing with minimum dimensions
        window.geometry("600x200")  # Initial size
        window.minsize(400, 150)  # Minimum size to ensure usability

        window.configure(background="black")
        window.wm_attributes("-alpha", 0.7)

        # Add dragging to window
        window.bind("<Button-1>", lambda e: self.on_drag_start(e, window))
        window.bind("<B1-Motion>", lambda e: self.on_drag_motion(e, window))

        # Create main frame with dynamic resizing
        main_frame = tk.Frame(window, bg='black')
        main_frame.pack(fill='both', expand=True, padx=2, pady=2)

        # Configure grid to resize
        for i in range(5):  # Number of rows
            main_frame.grid_rowconfigure(i, weight=1)
        for i in range(11):  # Maximum number of columns
            main_frame.grid_columnconfigure(i, weight=1)

        button_style = {
            'bg': "black",
            'fg': "white",
            'padx': 2,
            'pady': 2,
            'font': ('Arial', 12),
            'bd': 1
        }

        for y, row in enumerate(alphabets):
            for x, text in enumerate(row):
                if text == 'Shift':
                    width = 8
                    columnspan = 2
                elif text == 'Space':
                    width = 40
                    columnspan = 8
                elif text == 'Enter':
                    width = 8
                    columnspan = 2
                elif text == 'Back':
                    width = 8
                    columnspan = 2
                else:
                    width = 5
                    columnspan = 1

                button = tk.Button(
                    main_frame,
                    text=text,
                    width=width,
                    command=lambda value=text: self.select(entry, window, root, value),
                    **button_style
                )
                button.grid(row=y, column=x, columnspan=columnspan, padx=2, pady=2, sticky='nsew')
                button.bind("<Button-1>", lambda e, w=window: self.on_drag_start(e, w))
                button.bind("<B1-Motion>", lambda e, w=window: self.on_drag_motion(e, w))

        window.update_idletasks()  # Ensure window is fully created
        window.lift()  # Raise window to top
        entry.focus_set()  # Keep focus on entry
        return window

    def createNumaKey(self, root, entry, number=False):
        """Create numeric keyboard"""
        self.cleanup_keyboard()

        numbers = [
            ['1', '2', '3'],
            ['4', '5', '6'],
            ['7', '8', '9'],
            ['0', 'Enter', '<-']
        ]

        window = tk.Toplevel(root)
        window.attributes('-topmost', True)  # Make window stay on top
        self.current_window = window

        x = root.winfo_x()
        y = root.winfo_y()

        # Set initial size and allow resizing with minimum dimensions
        window.geometry("300x200")  # Initial size
        window.minsize(200, 150)  # Minimum size to ensure usability

        window.configure(background="cornflowerblue")
        window.wm_attributes("-alpha", 0.7)

        # Add dragging to window
        window.bind("<Button-1>", lambda e: self.on_drag_start(e, window))
        window.bind("<B1-Motion>", lambda e: self.on_drag_motion(e, window))

        # Create main frame with dynamic resizing
        main_frame = tk.Frame(window, bg='cornflowerblue')
        main_frame.pack(fill='both', expand=True, padx=2, pady=2)

        # Configure grid to resize
        for i in range(4):  # Number of rows
            main_frame.grid_rowconfigure(i, weight=1)
        for i in range(3):  # Number of columns
            main_frame.grid_columnconfigure(i, weight=1)

        button_style = {
            'width': 10,
            'padx': 3,
            'pady': 3,
            'bd': 12,
            'bg': "black",
            'fg': "white"
        }

        for y, row in enumerate(numbers):
            for x, text in enumerate(row):
                button = tk.Button(
                    main_frame,
                    text=text,
                    command=lambda value=text: self.select(entry, window, root, value),
                    **button_style
                )
                button.grid(row=y, column=x, padx=2, pady=2, sticky='nsew')

        window.update_idletasks()  # Ensure window is fully created
        window.lift()  # Raise window to top
        entry.focus_set()  # Keep focus on entry
        return window