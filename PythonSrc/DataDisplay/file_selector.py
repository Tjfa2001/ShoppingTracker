from tkinter import *
from tkinter import ttk
from tkinter import filedialog as fd
import os

#root = Tk()
#root.title("Select a file")

filename = fd.askopenfiles()

print(filename)
