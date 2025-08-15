import os
import json
import re

class FileHandler():

    directory = None

    def __init__(self):
        self.get_directory()
        self.compile_regex()

    def compile_regex(self):
        self.filename_search = re.compile(r"(\w+)\.(\w+)")

    def write_to_file(self,filename,json_receipt):
        match = self.filename_search.search(filename)
        new_name = match.group(1) + ".json"

        file_loc = os.path.join(self.directory,new_name)
        if os.path.isfile(file_loc):
            print("Cannot overwrite pre-existing file")
        else:
            with open(os.path.join(self.directory,new_name),"w") as file:
                file.write(json.dumps(json_receipt,indent = 4))

    def read_from_file(self,filename):
        
        file_loc = os.path.join(self.directory,filename)
    
        if os.path.isfile(file_loc):
            with open(os.path.join(self.directory,filename),"r") as file:
                text = file.read()
                return text
        else:
            print("File does not exist")

    def get_directory(self):
        self.directory = os.path.join(os.path.abspath("."),r"ShoppingTracker\ProcessedReceipts") 
        

if __name__ == '__main__':
    fh = FileHandler()
    print(fh.read_from_file("lidl_receipt1.json"))
