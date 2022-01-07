#! python3
from tkinter import *
from tkinter import ttk

import os
import random

from common import ExperimentFrame
from gui import GUI
from settings import CHARITY, CHARITIES, INSTRUCTIONS_CHARITIES



class Charity(ExperimentFrame):
    def __init__(self, root):
        super().__init__(root)          
      
        self.charity = StringVar()

        self.text = Text(self, font = "helvetica 18", relief = "flat", background = "white", height = 22,
                         wrap = "word", highlightbackground = "white", width = 80)
        self.text.grid(row = 1, column = 0, columnspan = 4)
        self.text.insert("1.0", INSTRUCTIONS_CHARITIES)
        self.text.config(state = "disabled")

        self.labels = {}
        self.rbuttons = {}
        for i, char in enumerate(CHARITIES):
            row = i + 4
            self.labels[i] = ttk.Label(self, text = char, background = "white", font = "helvetica 18")
            self.labels[i].grid(column = 1, row = row, pady = 2, sticky = W, padx = 20)
            self.rbuttons[i] = ttk.Radiobutton(self, text = "", variable = self.charity,
                                               value = char, command = self.checkCharity)
            self.rbuttons[i].grid(column = 2, row = row, sticky = W)

        ttk.Style().configure("TRadiobutton", background = "white", font = "helvetica 18")
        ttk.Style().configure("TButton", font = "helvetica 18")

        self.columnconfigure(0, weight = 1)
        self.columnconfigure(3, weight = 1)
        self.rowconfigure(0, weight = 1)
        self.rowconfigure(1, weight = 1)
        self.rowconfigure(9, weight = 1)
        self.rowconfigure(10, weight = 1)

        self.next = ttk.Button(self, text = "Continue", command = self.nextFun)
        self.next["state"] = "disabled"
        self.next.grid(row = 9, column = 0, columnspan = 4, pady = 15)


    def checkCharity(self):
        self.next["state"] = "!disabled"


    def write(self):
        self.file.write("Charity\n")
        charity = self.charity.get()
        self.root.texts["charity"] = charity
        self.file.write("\t".join([self.id, charity]) + "\n")


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.getcwd()))
    GUI([Charity])
