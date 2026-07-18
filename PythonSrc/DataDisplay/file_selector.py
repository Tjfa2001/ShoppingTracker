"""Simple module to select a file to process"""

from tkinter import filedialog as fd

filename = fd.askopenfiles()

print(filename)
