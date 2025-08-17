from tkinter import *
from tkinter import ttk
import tkinter as tk

class NameSelector():

    entry = None

    def __init__(self):
        root = Tk()
        root.geometry("250x250")
        entry = ttk.Entry(root)
        entry.pack()
        entry.bind("<Return>",self.test_func)
        self.entry = entry
        name = entry.get()
        print(name)
        root.mainloop()

    def test_func(self,e):
        name = e.widget.get()
        print(name)
        

NameSelector()