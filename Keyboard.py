import tkinter as tk
from globalvar import globaladc

class KeyBoard:
    def __init__(self):
        self.shift_active = False
        self._drag_data = {"x": 0, "y": 0, "width": 0, "height": 0}  # For dragging and resizing
        self.current_window = None  # Track current keyboard window
        self.current_entry = None  # Track current entry
        self.resizing = False  # Flag to indicate resize mode

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

    def on_resize_start(self, event, window):
        """Begin resize of the window with Ctrl key"""
        if event.state & 0x4:  # Check if Ctrl key is pressed (state & 0x4)
            self.resizing = True
            self._drag_data["x"] = event.x
            self._drag_data["y"] = event.y
            self._drag_data["width"] = window.winfo_width()
            self._drag_data["height"] = window.winfo_height()

    def on_drag_motion(self, event, window):
        """Handle dragging of the window"""
        if window.winfo_exists() and not self.resizing:  # Only drag if not resizing
            delta_x = event.x - self._drag_data["x"]
            delta_y = event.y - self._drag_data["y"]
            x = window.winfo_x() + delta_x
            y = window.winfo_y() + delta_y
            window.geometry(f"+{x}+{y}")
            window.lift()  # Keep window on top while dragging

    def on_resize_motion(self, event, window):
        """Handle resizing of the window with Ctrl key"""
        if window.winfo_exists() and self.resizing and (event.state & 0x4):  # Check Ctrl key
            delta_x = event.x - self._drag_data["x"]
            delta_y = event.y - self._drag_data["y"]
            new_width = max(400, self._drag_data["width"] + delta_x)  # Minimum width 400
            new_height = max(150, self._drag_data["height"] + delta_y)  # Minimum height 150
            window.geometry(f"{int(new_width)}x{int(new_height)}+{window.winfo_x()}+{window.winfo_y()}")
            window.lift()  # Keep window on top while resizing

    def on_release(self, event, window):
        """End resize or drag mode"""
        self.resizing = False

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
            ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', '-', '*'],
            ['Shift ^', 'z', 'x', 'c', 'v', 'b', 'n', 'm', '!', 'Back'],
            ['Space', 'Enter']
        ]

        window = tk.Toplevel(root)
        window.attributes('-topmost', True)  # Make window stay on top
        self.current_window = window

        x = root.winfo_x()
        y = root.winfo_y()

        window.geometry("+%d+%d" % (x+20, y+400))
        window.overrideredirect(1)  # Keep borderless for dragging
        window.configure(background="black")
        window.wm_attributes("-alpha", 0.7)

        # Add dragging and resizing bindings
        window.bind("<Button-1>", lambda e: self.on_drag_start(e, window))
        window.bind("<B1-Motion>", lambda e: self.on_drag_motion(e, window))
        window.bind("<Control-Button-1>", lambda e: self.on_resize_start(e, window))
        window.bind("<Control-B1-Motion>", lambda e: self.on_resize_motion(e, window))
        window.bind("<ButtonRelease-1>", lambda e: self.on_release(e, window))

        # Create main frame
        main_frame = tk.Frame(window, bg='black')
        main_frame.pack(padx=2, pady=2)

        button_style = {
            'bg': "black",
            'fg': "white",
            'padx': 2,
            'pady': 2,
            'font': ('Arial', 12),
            'bd': 1
        }

        for y, row in enumerate(alphabets):
            x = 0
            for text in row:
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
                button.bind("<Control-Button-1>", lambda e, w=window: self.on_resize_start(e, w))
                button.bind("<Control-B1-Motion>", lambda e, w=window: self.on_resize_motion(e, w))
                button.bind("<ButtonRelease-1>", lambda e, w=window: self.on_release(e, w))

                x += columnspan

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

        window.geometry("+%d+%d" % (x+40, y + 300))
        window.overrideredirect(1)  # Keep borderless for dragging
        window.configure(background="cornflowerblue")
        window.wm_attributes("-alpha", 0.7)

        # Add dragging and resizing bindings
        window.bind("<Button-1>", lambda e: self.on_drag_start(e, window))
        window.bind("<B1-Motion>", lambda e: self.on_drag_motion(e, window))
        window.bind("<Control-Button-1>", lambda e: self.on_resize_start(e, window))
        window.bind("<Control-B1-Motion>", lambda e: self.on_resize_motion(e, window))
        window.bind("<ButtonRelease-1>", lambda e: self.on_release(e, window))

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
                    window,
                    text=text,
                    command=lambda value=text: self.select(entry, window, root, value),
                    **button_style
                )
                button.grid(row=y, column=x, padx=2, pady=2, sticky='nsew')
                button.bind("<Button-1>", lambda e, w=window: self.on_drag_start(e, w))
                button.bind("<B1-Motion>", lambda e, w=window: self.on_drag_motion(e, w))
                button.bind("<Control-Button-1>", lambda e, w=window: self.on_resize_start(e, w))
                button.bind("<Control-B1-Motion>", lambda e, w=window: self.on_resize_motion(e, w))
                button.bind("<ButtonRelease-1>", lambda e, w=window: self.on_release(e, w))

        window.update_idletasks()  # Ensure window is fully created
        window.lift()  # Raise window to top
        entry.focus_set()  # Keep focus on entry
        return window