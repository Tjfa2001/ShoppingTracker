import tkinter as tk
import pandas as pd
import calendar
import matplotlib.pyplot as plt
from tkinter import ttk
from tkinter import *
import openpyxl
import config as cf
import PIL
from PIL import Image, ImageTk
import os
import sqlalchemy as sqa
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
    options_visible = True
    
    # Tkinter Components
    combo_mode = None
    option_panel = None
    content = None
    hide_option_button = None
    
    def __init__(self,connector,sql):
        self.sql = sql
        self.conn = connector
        self.root = tk.Tk()
        self.root.rowconfigure(0,weight=1)
        self.root.columnconfigure(0,weight=1)
        self.root.minsize(width=500,height=500)
        self.root.maxsize(width=2000,height=1250)
        self.mode = StringVar()
        
        self.loadSettings()
        
        # Content Frame is just a frame for the option panel and display panel to sit in
        self.make_content()
        self.content.grid(column=0,row=0,sticky="nsew")
        
        # Debug Style
        debug = ttk.Style()
        debug.configure(".",borderwidth=10, relief="solid", bordercolor="red")
        
        # Panel / frame for holding options chosen by user
        style = ttk.Style()
        style.configure("Option.TFrame",background="green")
        
        # Option Panel
        self.make_option_panel()
        self.option_panel.grid(column=0,row=0,ipadx=100,ipady=100,sticky="nsew")
        
        # Label with logo on it
        this_dir = os.path.dirname(os.path.abspath(__file__))
        logo_img_loc = os.path.join(this_dir,"Assets","LinkedInFinal2025.png")
        
        pil_img = Image.open(logo_img_loc)
        resized_pil = pil_img.resize((100,100),Image.Resampling.LANCZOS)
        
        image = ImageTk.PhotoImage(resized_pil)

        logo_label = ttk.Label(master=self.option_panel,
                               anchor="w",
                               image=image)
        logo_label.grid(row=0,column=0,sticky="nw")
        
        # Label asking for mode
        mode_option_label = ttk.Label(master=self.option_panel,
                                      text="How would you like to view your data?",
                                      anchor="center",wraplength=100)
        mode_option_label.grid(row=1,column=0,sticky="nsew")
        
        # Retrieve Button
        hide_option_button = ttk.Button(master=self.root,text="<>",command=self.hide_option,width=3)
        self.hide_option_button = hide_option_button
        hide_option_button.place(relx=0.3333, rely=0.5, anchor="center")
        
        # Combobox for mode
        self.make_combo()
        self.combo_mode.grid(row=2,column=0,padx=10,pady=10)
        
        # Button to retrieve data
        self.retrieve_button = ttk.Button(master=self.option_panel,text="Go",command=self.loadData)
        self.retrieve_button.grid(row=4,column=1)
        
        # Display panel
        self.make_display_panel()
        self.display_panel.grid(column=1,row=0,columnspan=2,sticky="nsew")
        
        label2 = ttk.Label(master=self.display_panel,text="Tom")
        label2.grid(row=0,column=0,sticky="ew")
        
        
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
    
    def hide_option(self):
        
        if self.options_visible:
            self.option_panel.grid_remove()
            self.options_visible = False
            self.hide_option_button.place(relx=0, rely=0.5, anchor="center")
            self.content.columnconfigure(0,weight=0,uniform="")
        else:
            self.option_panel.grid(column=0,row=0,ipadx=100,ipady=100,sticky="nsew")
            self.options_visible = True
            self.hide_option_button.place(relx=0.3333, rely=0.5, anchor="center")
            self.content.columnconfigure(0,weight=1,uniform="cols")
    
    def retrieve(self):
        print("Retrieving data...")
        
    def make_content(self):
        content = ttk.Frame(master=self.root)
        content.columnconfigure(0,weight=1,uniform="cols")
        content.columnconfigure(1,weight=1,uniform="cols")
        content.columnconfigure(2,weight=1,uniform="cols")
        content.rowconfigure(0,weight=1)
        content.grid_propagate(False)
        self.content = content
    
    def make_display_panel(self):
        display_panel = ttk.Frame(master=self.content,relief="sunken",borderwidth=15)
        self.display_panel = display_panel
    
    def make_option_panel(self):
        option_panel = ttk.Frame(master=self.content,relief="ridge",borderwidth=50,style="Option.TFrame")
        option_panel.propagate(False)
        option_panel.columnconfigure(0,weight=1)
        option_panel.rowconfigure(0,weight=1)
        option_panel.rowconfigure(1,weight=1)
        option_panel.rowconfigure(2,weight=1)
        option_panel.rowconfigure(3,weight=1)
        option_panel.rowconfigure(4,weight=1)
        option_panel.rowconfigure(5,weight=1)
        
        self.option_panel = option_panel
    
    def make_combo(self):
        combo_mode = ttk.Combobox(master=self.option_panel,textvariable=self.mode)
        combo_mode.configure(values=("Weekly","Monthly","Yearly"),state="readonly")
        combo_mode.set("Weekly")
        combo_mode.bind('<Return>',self.printcombo)
        self.combo_mode = combo_mode
    
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
        match self.combo_mode.current():
            # Monthly
            case 1:
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
        canvas = FigureCanvasTkAgg(fig,master = self.display_panel)  
        canvas.draw()
        
        if self.canvas:
            self.canvas.get_tk_widget().destroy()
            
        self.canvas = canvas
        
        # placing the canvas on the Tkinter window
        print("Trying to grid")
        canvas.get_tk_widget().grid(row=1,column=1)

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
    
    engine = sqa.create_engine("postgresql://postgres:postgres@localhost/lidl_receipts")
    connect = engine.connect()
    dd = DataDisplayer(connector=connect, sql=cf.monthSQL)