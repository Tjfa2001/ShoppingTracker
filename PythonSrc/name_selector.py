from tkinter import *
from tkinter import ttk
import tkinter as tk
import master_dictionary as md

class NameSelector():

    entry = None
    master_dictionary = None
    new_name = None

    def __init__(self,item):
        self.item_confirm(item)
        self.master_dictionary = md.MasterDict()

    def add_to_dictionary(self,e,item):
        new_item = e.widget.get()
        self.new_name = new_item
        self.root.destroy()
        
    def item_confirm(self,item):
        self.root = Tk()
        self.root.geometry("750x150")
        label = ttk.Label(self.root,text=f"What would you like {item} to be called?",font=("Arial",15))
        label.pack()
        entry = ttk.Entry(self.root,width=20,font=("Arial",15))
        entry.pack()

        label2 = ttk.Label(self.root,text="Press Enter / Return to confirm",font=("Arial",15))
        label2.pack()
        entry.bind("<Return>",lambda e: self.add_to_dictionary(e,item))
        mainloop()

if __name__ == "__main__":
    name_selector = NameSelector("Test Item")
    print(name_selector.new_name)
    #print(name_selector.master_dictionary.master)
    #name_selector.master_dictionary.write_to_file(name_selector.master_dictionary.master)