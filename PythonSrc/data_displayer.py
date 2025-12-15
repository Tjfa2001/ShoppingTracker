import tkinter as tk
import pandas as pd
import matplotlib.pyplot as plt
from tkinter import ttk
import openpyxl
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, 
NavigationToolbar2Tk)

class DataDisplayer():
    
    root = None
    conn = None
    data = None
    sql = None
    
    def __init__(self,connector,sql):
        self.sql = sql
        self.conn = connector
        self.root = tk.Tk()
        self.root.title = "Data Displayer 1.0"
        self.root.geometry("1000x1000")
        self.loadData()
        time_combo = ttk.Combobox(master=self.root,values=["Year","Month","Day"])
        time_combo.pack()
        destroy = tk.Button(self.root,command=self.loadData,text='Load Data',width=50)
        destroy.pack()
        #self.root.mainloop()
    
    def loadData(self):
        data = pd.read_sql(sql=self.sql,con=self.conn.connection)
        self.data = data
        print(data)
        #self.data['spend'] = data['spend'].apply(lambda x: round(x, 2))
        #self.writeDataToFile(self.data)
        
    def writeDataToFile(self,dataframe:pd.DataFrame):
        print(dataframe)
        dataframe.to_csv('dataframe.csv',index=False)
        dataframe.to_excel('dataframe.xlsx')
        
    """
    def displayData(self):
        fig = Figure(figsize=(3,3))
        x_list=[0,1,2,3]
        y=[2,5,10,25]
        figur = plt.plot(x_list,y)
        # creating the Tkinter canvas
        # containing the Matplotlib figure
        canvas = FigureCanvasTkAgg(figur,master = self.root)  
        canvas.draw()

        # placing the canvas on the Tkinter window
        canvas.get_tk_widget().pack()

        # creating the Matplotlib toolbar
        toolbar = NavigationToolbar2Tk(canvas,self.root)
        toolbar.update()

        # placing the toolbar on the Tkinter window
        canvas.get_tk_widget().pack()
        plt.show()
    """
        
    def landingPage(self):
        pass