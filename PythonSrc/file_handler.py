import os
import json
import re

class FileHandler():

    processed_directory = None
    receipt_directory = None
    accepted_directory = None
    excluded_directory = None
    log_directory = None

    def __init__(self):
        self.get_directories()
        self.compile_regex()

    def compile_regex(self):
        self.filename_search = re.compile(r"(\w+)\.(\w+)")

    def write_logger_to_file(self,logger):
        log_name = "log"
        with open(os.path.join(self.log_directory,log_name),'w') as file:
            for line in logger.log:
                file.write(f"{line}\n")

    def rename(self,new_name,old_name):
        os.rename(old_name,new_name)

    def write_json_receipt_to_file(self,filename,json_receipt):

        match = self.filename_search.search(filename)
        new_name = match.group(1) + ".json"

        file_loc = os.path.join(self.processed_directory,new_name)
        if os.path.isfile(file_loc):
            #print("Cannot overwrite pre-existing file")
            with open(os.path.join(self.processed_directory,new_name),"w") as file:
                file.write(json.dumps(json_receipt,indent = 4))
        else:
            with open(os.path.join(self.processed_directory,new_name),"w") as file:
                file.write(json.dumps(json_receipt,indent = 4))

    def accept(self,filename):
        accepted_loc = os.path.join(self.accepted_directory,filename)
        receipt_loc = os.path.join(self.receipt_directory,filename)
        os.rename(receipt_loc,accepted_loc)

    def exclude(self,filename):    
        excluded_loc = os.path.join(self.excluded_directory,filename)
        receipt_loc = os.path.join(self.receipt_directory,filename)
        os.rename(receipt_loc,excluded_loc)

    def read_from_file(self,filename):
        
        file_loc = os.path.join(self.processed_directory,filename)
    
        if os.path.isfile(file_loc):
            with open(os.path.join(self.processed_directory,filename),"r") as file:
                text = file.read()
                return text
        else:
            print("File does not exist")

    def get_directories(self):
        self.processed_directory = os.path.join(os.path.abspath("."),r"ShoppingTracker\ProcessedReceipts") 
        self.receipt_directory = os.path.join(os.path.abspath("."),r"ShoppingTracker\Receipts")
        self.accepted_directory = os.path.join(os.path.abspath("."),r"ShoppingTracker\Accepted")
        self.excluded_directory = os.path.join(os.path.abspath("."),r"ShoppingTracker\Excluded")
        self.log_directory = os.path.join(os.path.abspath("."),r"ShoppingTracker\Logs")
        

if __name__ == '__main__':
    fh = FileHandler()
    print(fh.read_from_file("lidl_receipt1.json"))
