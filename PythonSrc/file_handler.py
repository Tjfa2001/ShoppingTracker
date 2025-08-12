import os
import json
import re

class File_Handler():

    directory = None

    def __init__(self):
        self.get_directory()

    def write_to_file(self,filename,json_receipt):
        match = re.search(r"(\w+)\.(\w+)",filename)
        new_name = match.group(1) + ".json"

        with open(os.path.join(self.directory,new_name),"w") as file:
            file.write(json.dumps(json_receipt,indent = 4))

    def get_directory(self):
        self.directory = os.path.join(os.path.abspath("."),r"ShoppingTracker\ProcessedReceipts") 
