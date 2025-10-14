from tkinter import *
from tkinter.ttk import *
import tkinter as tk
import os
import json
#import PythonSrc.file_handler as fh

class CategoryAssigner():
    
    item_name = ""
    category = ""
    categories = []
    
    def __init__(self, item_name):
        self.item_name = item_name
        self.category = None
        self.open_item_file()
        self.retrieve_item()
        self.retrieve_category(text=f"What category does {self.item_name} belong to?")
        self.retrieve_category(text=f"Which category do you want to remove?")
        self.remove_category()
        self.category = "Frozen Foods"
        self.add_category()
    
    def __init__(self):
        self.item_name = None
        self.category = None
        self.open_item_file()
        
    def add_category(self):
        self.categories.append(self.category)
        self.categories = sorted(self.categories)
        print(self.categories)
        self.write_categories_to_file()   
    
    def get_category(self):
        return self.category
    
    def set_item(self, e, Listbox):
        selected_index = Listbox.curselection()
        if selected_index:
            self.item_name = Listbox.get(selected_index)
            self.root.destroy()
        else:
            print("No item selected.")
            
    def retrieve_item(self):
        self.root = tk.Tk()
        self.root.geometry("500x1000")
        label = tk.Label(self.root, text="Which item would you like to assign a category to?", font=("Arial", 15))
        label.pack(pady=20)
        Listbox = tk.Listbox(self.root, font=("Arial", 15), height=50, width=30)
        Listbox.pack(pady=10)
        items = self.open_item_file()
        for item in items:
            Listbox.insert(tk.END, item)    
        Listbox.bind("<Double-Button-1>", lambda e: self.set_item(e, Listbox))
        tk.mainloop()
        
    def remove_category(self):
        if not self.category:
            self.retrieve_category(text=f"Which category do you want to remove?")
        
        self.categories.remove(self.category)
        self.write_categories_to_file()
            
        
    def retrieve_category(self,text):
        # Setting up the GUI
        self.root = tk.Tk()
        self.root.geometry("700x350")
        label = tk.Label(self.root, text=text, font=("Arial", 15))
        label.pack(pady=20)
        Listbox = tk.Listbox(self.root, font=("Arial", 15), height=10)

        #categories = self.open_category_file()
        categories = sorted(self.open_category_file())
        if not categories:
            categories = ["No categories found","Please add some"]
        
        self.categories = categories
        for category in categories:
            Listbox.insert(tk.END, category)
        Listbox.pack(pady=10)
        Listbox.bind("<Double-Button-1>", lambda e: self.set_category(e, Listbox))
        tk.mainloop()
        pass
    
    def open_category_file(self):
        
        # Get the absolute path to categories.txt
        category_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__),"categories.txt"))

        # Check if the file exists before trying to open it
        if os.path.isfile(category_file_path):
            with open(category_file_path, "r") as file:
                categories = file.read().splitlines()
                return categories
        else:
            return []
    
    def open_item_file(self):
        item_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__),"..\\..\\MasterDictionary\\MastDict.json"))
        
        if os.path.isfile(item_file_path):
            with open(item_file_path,"r") as file:
                data = json.load(file)
                items = data.values()
                return sorted(list(items))
        else:
            return ["No items found","Please add some"]

    def write_categories_to_file(self):
        path = os.path.abspath(os.path.join(os.path.dirname(__file__),"categories.txt"))
        with open(path, "w") as file:
            file.write("\n".join(self.categories))

    def set_category(self, e, Listbox):
        selected_index = Listbox.curselection()
        if selected_index:
            self.category = Listbox.get(selected_index)
            self.root.destroy()
            print(f"Selected category: {self.category}")
        else:
            print("No category selected.")
            exit(1)
            
    def view_categories(self):
        categories = self.open_category_file()
        print("Current categories:")
        for category in categories:
            print(f"- {category}")
            
if __name__ == "__main__":
    category_assigner = CategoryAssigner("Beetroot")
    #print(category_assigner.get_category())