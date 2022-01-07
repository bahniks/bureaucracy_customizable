from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from time import localtime, strftime, time
from collections import defaultdict

import os

from settings import TESTING, SCREENWIDTH, SCREENHEIGHT


class GUI(Tk):
    def __init__(self, frames):
        super().__init__()
        
        self.title("Experiment")
        self.config(bg = "white")
        if TESTING:
            self.geometry("{}x{}".format(SCREENWIDTH, SCREENHEIGHT))
        self.attributes("-fullscreen", not TESTING)
        self.attributes("-topmost", not TESTING)
        self.overrideredirect(not TESTING)
        self.protocol("WM_DELETE_WINDOW", lambda: self.closeFun())

        self.screenwidth = SCREENWIDTH
        self.screenheight = SCREENHEIGHT

        filepath = os.path.join(os.getcwd(), "Data")
        if not os.path.exists(filepath):
            os.mkdir(filepath)
        
        writeTime = localtime()
        self.outputfile = os.path.join(filepath, strftime("%y_%m_%d_%H%M%S", writeTime) + ".txt")

        self.bind("<Escape>", self.closeFun)

        self.order = frames

        self.texts = defaultdict(str)
                                    
        self.count = -1

        self.columnconfigure(0, weight = 1)
        self.rowconfigure(0, weight = 1)
                      
        with open(self.outputfile, mode = "w") as self.file:
            self.nextFrame()
            self.mainloop()
        

    def nextFrame(self):
        self.file.write("time: " + str(time()) + "\n")
        self.count += 1
        if self.count >= len(self.order):
            self.destroy()
        else:
            nxt = self.order[self.count]
            if isinstance(nxt, tuple):
                self.frame = nxt[0](self, **nxt[1])
            else:
                self.frame = nxt(self)
            self.frame.grid(row = 0, column = 0, sticky = (N, S, E, W))

            if hasattr(self.frame, "run"):
                self.update()
                self.frame.run()


    def closeFun(self, event = ""):
        if TESTING:
            self.destroy()
            return
        
        message = "Are you sure you want to end the experiment? "
        ans = messagebox.askyesno(message = message, icon = "question", parent = self,
                                  title = "End the experiment?")
        if ans:
            self.destroy() 
