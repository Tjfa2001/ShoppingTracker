"""Module to display data of loaded receipts"""

from warnings import deprecated
import tkinter as tk
import calendar
from tkinter import ttk
from tkinter import *
from PIL import Image, ImageTk
import os
import sqlalchemy as sqa
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import config as cf
from DataDisplay import option_panel as op
import matplotlib.pyplot as plt

class DataDisplayer():

    """Main Tkinter window to display loaded receipt data"""
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
    image = None
    retrieve_button = None

    def __init__(self,connector,sql):

        # SQL Query to be run
        self.sql = sql

        # Connection to the database
        self.conn = connector

        # Main frame for holding other frames
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

        # Make options panel
        self.option_panel = op.OptionPanel(self.content)
        self.option_panel.grid(column=0,row=0,sticky="nsew",ipadx=10,ipady=10)

        # Hide option panel
        self.hide_option_button = ttk.Button(master=self.root,text="<>",
                                             command=self.hide_option,width=3)
        self.hide_option_button.place(relx=0.3333, rely=0.5, anchor="center")

        # Combobox for mode
        self.combo_mode = self.option_panel.make_combo_mode_box(mode=self.mode)
        self.combo_mode.grid(row=2,column=0,padx=10,pady=10)

        # Button to retrieve data
        self.retrieve_button = self.option_panel.make_retrieve_button(command=self.retrieve)

        # Display panel
        self.make_display_panel()
        self.display_panel.grid(column=1,row=0,columnspan=2,sticky="nsew")

        self.root.mainloop()

    def hide_option(self):

        """Hides the options menu from the user"""

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

        """Retrieves the data from the database"""
        print("Retrieving data...")

    def make_content(self):
        """Makes the content panel of the data displayer"""
        content = ttk.Frame(master=self.root)
        content.columnconfigure(0,weight=1,uniform="cols")
        content.columnconfigure(1,weight=1,uniform="cols")
        content.columnconfigure(2,weight=1,uniform="cols")
        content.rowconfigure(0,weight=1)
        content.grid_propagate(False)
        self.content = content

    def make_display_panel(self):
        """Makes the display panel of the data displayer"""
        display_panel = ttk.Frame(master=self.content,relief="sunken",borderwidth=15)
        self.display_panel = display_panel

    def printcombo(self,event):
        """Prints the combo box mode selected"""
        print(self.mode.get())
        print(event)

    def loadSettings(self):
        """Loads settings from the config file"""
        self.root.geometry(cf.DATA_DISPLAYER_GEOMETRY)
        self.root.title = cf.DATA_DISPLAYER_TITLE

    def load_data(self):
        """Load data from the database"""
        data = pd.read_sql(sql=self.sql,con=self.conn.connection)
        self.data = data
        match self.combo_mode.current():
            # Monthly
            case 1:
                if self.first:
                    self.extractMonthData(9,2025)
                    self.first = False
                else:
                    month = int(input("What is the month you would like to look at?"))
                    year = int(input("What year would you like to look at?"))
                    self.extractMonthData(month,year)
            case _:
                pass

    @deprecated("Use Data Displayer instead")
    def write_data_to_file(self,dataframe:pd.DataFrame):
        """Write data to a csv file and xlsx file"""
        dataframe.to_csv('dataframe.csv',index=False)
        dataframe.to_excel('dataframe.xlsx')

    def display_data_for_month(self,month_data,month,year):

        """Displays data for a given month"""
        fig = Figure(figsize=(10,5))

        #categories = self.data['category']
        #cost = self.data['total_cost']
        axis1 = fig.add_subplot(111)
        axis1.clear()

        # This is where the data will need to be loaded into a plot
        colours = ['r','b','g','pink','orange','black']

        month_category = month_data['category']
        month_cost = month_data['total_cost']
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
        self.display_data_for_month(monthsData,month,year)

if __name__ == '__main__':
    import DataDisplay as dd
    print("This module is not intended to be run directly")

    engine = sqa.create_engine("postgresql://postgres:postgres@localhost/lidl_receipts")
    connect = engine.connect()
    dd = DataDisplayer(connector=connect, sql=cf.MONTHLY_DATA_SQL)
