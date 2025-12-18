import tkinter as tk
import pandas as pd
import calendar
import matplotlib.pyplot as plt
from tkinter import ttk
import openpyxl
import config as cf
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, 
NavigationToolbar2Tk)

class DataDisplayer():
    
    # This is the main Tkinter window
    root = None
    conn = None
    data = None
    sql = None
    canvas = None
    time_combo = None
    first = True
    
    def __init__(self,connector,sql):
        self.sql = sql
        self.conn = connector
        self.root = tk.Tk()
        
        # Loads settings from the config file
        self.loadSettings()
        
        time_combo = ttk.Combobox(master=self.root,values=["Year","Month","Day"])
        time_combo.pack()
        load = tk.Button(self.root,command=self.loadData,text='Load Data',width=50)
        load.pack()
        display = tk.Button(self.root,command=self.displayDataForMonth,text='Display Data',width=50)
        display.pack()
        self.root.mainloop()
    
    def loadSettings(self):
        self.root.geometry(cf.geometry)
        self.root.title = cf.dataDisplayerTitle
        pass
    
    def loadData(self):
        data = pd.read_sql(sql=self.sql,con=self.conn.connection)
        self.data = data
        if self.first == True:
            self.extractMonthData(9,2025)
            self.first = False
        else:
            self.extractMonthData(12,2025)
        
    def writeDataToFile(self,dataframe:pd.DataFrame):
        print(dataframe)
        dataframe.to_csv('dataframe.csv',index=False)
        dataframe.to_excel('dataframe.xlsx')
    
    def displayDataForMonth(self,monthData,month,year):
        fig = Figure(figsize=(10,5))
        
        categories = self.data['category']
        cost = self.data['total_cost']
        axis1 = fig.add_subplot(111)
        axis1.clear()
        
        # This is where the data will need to be loaded into a plot
        colours = ['r','b','g','pink','orange','black']
        
        month_category = monthData['category']
        month_cost = monthData['total_cost']
        axis1.bar(month_category,month_cost,0.4,color=colours,label="Toms")
        axis1.set_ylabel("Total Spend (£)")
        axis1.set_xlabel("Item Categories")
        axis1.set_title(f"Spend at Lidl in {calendar.month_name[month]} {year}")
            
        plt.setp(axis1.get_xticklabels(), rotation=45, ha="right")
        fig.subplots_adjust(bottom=0.25)

        # creating the Tkinter canvas
        # containing the Matplotlib figure
        canvas = FigureCanvasTkAgg(fig,master = self.root)  
        canvas.draw()
        
        if self.canvas:
            self.canvas.get_tk_widget().destroy()
            
        self.canvas = canvas
        
        # placing the canvas on the Tkinter window
        canvas.get_tk_widget().pack()

        # creating the Matplotlib toolbar
        #toolbar = NavigationToolbar2Tk(canvas,self.root)
        #toolbar.update()
        plt.show()
    
    def extractMonthData(self,month:int, year:int):
        monthsData = self.data[(self.data["month"]==month) & (self.data["year"]==year)]
        self.displayDataForMonth(monthsData,month,year)
        
    def landingPage(self):
        pass
    
    def clearChart(self):
        pass
    
if __name__ == '__main__':
    print("This module is not intended to be run directly")