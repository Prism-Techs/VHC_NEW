import tkinter as tk
from globalvar import globaladc

class KeyBoard:

    def select(self, entry, window, mainwindow, value, ucase=None):        
        uppercase =ucase
        if value == "Space":
            value = ' '
        elif value == 'Enter':
            value = ''
            globaladc.get_print("enter pressed")
            mainwindow.focus_force()
            window.destroy()
        elif value == 'Tab':
            value = '\t'

        if value == "Back" or value == '<-':
            if isinstance(entry, tk.Entry):
                entry.delete(len(entry.get())-1, 'end')
            #elif isinstance(entry, tk.Text):
            else: # tk.Text
                entry.delete('end - 2c', 'end')
        elif value in ('Caps Lock', 'Shift'):
            uppercase = not uppercase # change True to False, or False to True
        else:
            if uppercase:
                value = value.upper()
            entry.insert('end', value)
        globaladc.buzzer_1()

   # create a Alpah and numeric keyboard
    def createAlphaKey(self, root, entry, number=False):

        alphabets = [
            [ 'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
            [ 'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'Back'],
            [ 'Z', 'X', 'C', 'V', 'B', 'N', 'M','Enter'],
            ['Space']
        ]
        
        window = tk.Toplevel(root)
        x = root.winfo_x()
        y = root.winfo_y()

        window.geometry("+%d+%d" %(x+20, y+400))

        window.overrideredirect (1)  # Don't allow the widgets inside to determine the frame's width / height
        
        window.configure(background="black")
        window.wm_attributes("-alpha", 0.7)

        for y, row in enumerate(alphabets):

            x = 0

            #for x, text in enumerate(row):
            for text in row:
                if text == 'Shift':
                    width = 12
                    columnspan = 2
                elif text == 'Space':
                    width = 80
                    columnspan = 16
                elif text == 'Enter':
                    width = 10
                    columnspan = 1
                else:
                    width = 8
                    columnspan = 1

                tk.Button(window, text=text, width=width,
                          command=lambda value=text: self.select(entry, window,root,value),
                          padx=3, pady=3, bd=12, bg="black", fg="white"
                         ).grid(row=y, column=x, columnspan=columnspan)

                x += columnspan
        

   #create a Numeric Keypad
    def createNumaKey(self, root, entry, number=False):

            numbers = [
                ['1', '2', '3' ],
                ['4', '5', '6' ],
                ['7', '8', '9',],
                ['0', 'Enter','<-']
            ]


            window = tk.Toplevel(root)
            x = root.winfo_x()
            y = root.winfo_y()

            window.geometry("+%d+%d" % (x+40, y + 300))

            window.overrideredirect (1)  # Don't allow the widgets inside to determine the frame's width / height

            window.configure(background="cornflowerblue")
            window.wm_attributes("-alpha", 0.7)

            for y, row in enumerate(numbers):

                x = 0
                width = 10
                columnspan = 1
                #for x, text in enumerate(row):
                for text in row:
                    # if text in ('Enter', 'Shift'):
                        
                    #     columnspan = 1
                    # elif text == 'Space':
                    #     width = 8
                    #     columnspan = 1
                    # else:
                    #     width = 8
                    #     columnspan = 1

                    tk.Button(window, text=text, width=width,
                            command=lambda value=text: self.select(entry, window,root,value),
                            padx=3, pady=3, bd=12, bg="black", fg="white"
                            ).grid(row=y, column=x, columnspan=columnspan)

                    x += columnspan

# --- main ---

if __name__ == '__main__':
    root = tk.Tk()
    root.title('Test Keyboard')
    kb = KeyBoard()

    def callback(sv):
        lobaladc.get_print("call back")

    label = tk.Label(root, text='Test Keyboard')
    label.grid(row=0, column=0, columnspan=2)

    sv = tk.StringVar ()
    sv.trace ("w",
              lambda name, index, mode, sv=sv: callback (sv))

    entry1 = tk.Entry(root)
    entry1.bind ('<FocusIn>',
                   lambda event: kb.createAlphaKey(root, entry1))
    entry1.grid(row=1, column=0, sticky='news')

    button1 = tk.Button(root, text='Keyboard', command=lambda:kb.createNumaKey(root, entry1))
    button1.grid(row=1, column=1, sticky='news')

    entry2 = tk.Entry(root)
    entry2.grid(row=2, column=0, sticky='news')

    button2 = tk.Button(root, text='Keyboard', command=lambda:kb.createNumaKey(root, entry2))
    button2.grid(row=2, column=1, sticky='news')

    text1 = tk.Text(root)
    text1.grid(row=3, column=0, sticky='news')

    button3 = tk.Button(root, text='Keyboard', command=lambda:kb.createNumaKey(root, text1))
    button3.grid(row=3, column=1, sticky='news')

    root.mainloop()