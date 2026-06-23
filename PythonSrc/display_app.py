from tkinter import *
from tkinter import ttk
import tkinter as tk
import config as cf
import os

from DataDisplay import option_panel as op
from DataDisplay import retrieve_button as rb
from DataDisplay.dim_handler import DimHandler

class DisplayApp:
    
    def __init__(self):
        # Main frame for holding other frames
        self.root = tk.Tk()
        self.root.rowconfigure(0,weight=1)
        self.root.columnconfigure(0,weight=1)
        
        self.load_settings()
        self._build()
        self.run()
        
    def _build(self):
        
        content = ttk.Frame(master=self.root)
        content.columnconfigure(0,weight=1,uniform="cols")
        content.columnconfigure(1,weight=1,uniform="cols")
        content.columnconfigure(2,weight=1,uniform="cols")
        content.rowconfigure(0,weight=1)
        content.grid_propagate(False)
        self.content = content
        self.content.grid(column=0,row=0,sticky="nsew")
        
        # Debug Style
        debug = ttk.Style()
        debug.configure(".",borderwidth=10, relief="solid", bordercolor="red")
     
        # Make options panel
        self.option_panel = op.OptionPanel(self.content)
        self.option_panel.grid(column=0,row=0,sticky="nsew",ipadx=10,ipady=10)
        
        # Hide option panel
        self.hide_option_button = ttk.Button(master=self.root,text="<>",width=3)
        self.hide_option_button.place(relx=0.3333, rely=0.5, anchor="center")
        
        # Button to retrieve data
        self.retrieve_button = rb.RetrieveButton(parent=self.option_panel, text="Retrieve Data", command=self.retrieve_data)
        self.retrieve_button.grid(column=1,row=3,padx=50, pady=50)
        
        # Display panel
        #self.make_display_panel()
        #self.display_panel.grid(column=1,row=0,columnspan=2,sticky="nsew")
        
    def load_settings(self):
        min_dim = DimHandler.get_dims(cf.DATA_DISPLAY_MIN_DIM)
        max_dim = DimHandler.get_dims(cf.DATA_DISPLAY_MAX_DIM)
        
        self.root.minsize(width=min_dim[0],height=min_dim[1])
        self.root.maxsize(width=max_dim[0],height=max_dim[1])
        self.root.geometry(cf.DATA_DISPLAY_MAX_DIM)
        
        self.root.title = cf.DATA_DISPLAY_TITLE
    
    def retrieve_data(self):
        print("Retrieving")
        
    def run(self):
        self.root.mainloop()
        
if __name__ == '__main__':
    print(f"Running {os.path.basename(__file__)} directly")
    
    da = DisplayApp()