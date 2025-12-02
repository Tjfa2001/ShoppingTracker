import tkinter as tk
import pandas as pd
from tkinter import ttk

class DataDisplayer():
    
    root = None
    conn = None
    
    def __init__(self,connector):
        self.conn = connector
        self.root = tk.Tk()
        self.root.title = "Data Displayer 1.0"
        destroy = tk.Button(self.root,command=self.loadData,text='Destroy!',width=50)
        destroy.pack()
        self.root.mainloop()
    
    def loadData(self):
        data = pd.read_sql("SELECT * FROM lidl.items;",con=self.conn.connection,chunksize=10)
        for a in data:
            print(a)
        
    def landingPage(self):
        pass