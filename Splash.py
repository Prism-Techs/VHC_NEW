import tkinter as tk

class Splash(tk.Toplevel):
    def __init__(self, parent):
        tk.Toplevel.__init__(self, parent)
        self.title("Macular Metrics")

        ## required to make window show before the program gets to the mainloop
        self.update()
