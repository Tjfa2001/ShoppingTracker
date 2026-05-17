import tkinter as tk
import pandas as pd
import calendar
import matplotlib.pyplot as plt
from tkinter import ttk
from tkinter import *
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
    mode = None
    
    def __init__(self,connector,sql):
        self.sql = sql
        self.conn = connector
        self.root = tk.Tk()
        self.root.rowconfigure(0,weight=1)
        self.root.columnconfigure(0,weight=1)
        self.root.minsize(width=500,height=500)
        self.root.maxsize(width=1500,height=1250)
        self.mode = StringVar()
        
        self.loadSettings()
        
        content = ttk.Frame(master=self.root)
        content.grid(column=0,row=0,sticky="nsew")
        content.columnconfigure(0,weight=1)
        content.rowconfigure(0,weight=1)
        content.columnconfigure(1,weight=1)
        content.grid_propagate(False)
        
        # Panel / frame for holding options chosen by user
        style = ttk.Style()
        style.configure("Option.TFrame",background="lightskyblue")
        
        option_panel = ttk.Frame(master=content,relief="ridge",borderwidth=50,style="Option.TFrame")
        option_panel.grid(column=0,row=0,ipadx=10,ipady=10,sticky="nsew")
        option_panel.propagate(False)
        
        # Label asking for mode
        mode_option_label = ttk.Label(master=option_panel,text="How would you like to view your data?")
        mode_option_label.grid(row=1,column=0)
        
        # Combobox for mode
        combo_mode = ttk.Combobox(master=option_panel,textvariable=self.mode)
        combo_mode.configure(values=("Monthly","Weekly","Yearly"),state="readonly")
        combo_mode.grid(row=2,column=0)
        combo_mode.bind('<Return>',self.printcombo)
        
        display_panel = ttk.Frame(master=content,relief="sunken",borderwidth=15)
        display_panel.grid(column=1,row=0,sticky="nsew")
        
        """
        content2 = tk.Frame(master=self.root,padx=10,pady=10,bg="green",relief='raised')
        content2.place(relx=0,rely=0,relwidth=0.3,relheight=1.0)
        content2.grid_propagate(False)
        
        button = tk.Button(master=content2,text="Hello",command=self.example_function)
        button.grid()
        
        button.bind('<Enter>',lambda e: button.configure(text="Entered"))
        button.bind('<Leave>',lambda e: button.configure(text="Left"))
        
        options_label = tk.Label(master=content2,text="Options Panel")
        
        frame_two = tk.Frame(master=self.root,background="red")
        frame_two.grid(column=1,row=1,columnspan=2,rowspan=2)
        #left_frame = tk.Frame(master = content,bg='skyblue',width=100,height=300)
        
        #frame.pack(padx=100, pady=100,fill='x',side=tk.LEFT)
        """
        
        """
        frame2 = tk.Frame(master = self.root, bg='red',width=500, height=500)
        #frame2.pack(padx=50,pady=50,side=tk.RIGHT,fill='y')
        
        left_button = tk.Button(master=frame2,text="<",width=50,height=50)
        right_button = tk.Button(master=frame2,text=">",width=50,height=50)
        
        #left_button.pack()
        #right_button.pack()
        # Loads settings from the config file
        self.loadSettings()
        
        time_combo = ttk.Combobox(master=self.root,values=["Year","Month","Day"])
        #time_combo.pack()
        
        load_button = tk.Button(self.root,command=self.loadData,text='Load Data',width=50)
        #load_button.pack()
        
        display = tk.Button(self.root,command=self.displayDataForMonth,text='Display Data',width=50)
        #display.pack()
        
        frame.grid(column=0,row=0)
        """

        #left_frame.grid(column=0,row=3)
        #options_label.grid(column=1,row=1)
        
        self.root.mainloop()
    
    def printcombo(self,event):
        print(self.mode.get())
        print(event)

    def example_function(self):
        print("HELLO")
    
    def loadSettings(self):
        self.root.title("Receipt Data Displayer")
        self.root.geometry(cf.geometry)
        self.root.title = cf.dataDisplayerTitle
    
    def loadData(self):
        data = pd.read_sql(sql=self.sql,con=self.conn.connection)
        self.data = data
        match self.mode:
            case "Month Grouping":
                if self.first == True:
                    self.extractMonthData(9,2025)
                    self.first = False
                else:
                    month = int(input("What is the month you would like to look at?"))
                    year = int(input("What year would you like to look at?"))
                    self.extractMonthData(month,year)
            case _:
                pass
        
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
    dd = DataDisplayer(connector="abc", sql="abc")