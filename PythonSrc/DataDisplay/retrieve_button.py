import tkinter as tk
from tkinter import *
from tkinter import ttk

class RetrieveButton(ttk.Button):
    
    def __init__(self,parent,command=None,width=50,height=50,text="Button"):
        super().__init__(parent,text=text,width=width,command=command)
                  
    