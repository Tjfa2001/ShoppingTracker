import os
import json
import re

class FileHandler():

    directory = None

    def __init__(self):
        self.get_directory()

    def write_to_file(self,filename,json_receipt):
        match = re.search(r"(\w+)\.(\w+)",filename)
        new_name = match.group(1) + ".json"

        with open(os.path.join(self.directory,new_name),"w") as file:
            file.write(json.dumps(json_receipt,indent = 4))

    def read_from_file(self,filename):

        with open(os.path.join(self.directory,filename),"r") as file:
            text = file.read()
            return text

    def get_directory(self):
        self.directory = os.path.join(os.path.abspath("."),r"ShoppingTracker\ProcessedReceipts") 
        

if __name__ == '__main__':
    fh = FileHandler()
    fh.read_from_file("lidl_receipt1.json")
