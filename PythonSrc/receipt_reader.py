import pytesseract
import cv2
from PIL import Image
import os
import re
#import my_logger as logger
import sys
import json
import file_handler as fh
import numpy as np

class ReceiptReader:

    receipts = []
    logger = None
    file_handler = None
    abspath = os.path.abspath(".")
    receipt_dir = os.path.join(abspath,r"ShoppingTracker\Receipts")
    excluded_dir = os.path.join(abspath,r"ShoppingTracker\Excluded")
    accepted_dir = os.path.join(abspath,r"ShoppingTracker\Accepted")

    def __init__(self,logger):
        self.compile_regex()
        self.logger = logger
        self.file_handler = fh.FileHandler()

    def get_receipts(self):

        receipts = []
        excluded_files = []

        for file in os.listdir(self.receipt_dir):
            
            receipt_loc = os.path.join(self.receipt_dir,file)

            pass_extension_check = self.file_extension_check(file)
            pass_openable_photo_check = self.open_photo_check(file,self.receipt_dir)
            self.name_check(file)

            if pass_extension_check and pass_openable_photo_check:
                receipts.append(file)

            else:
                excluded_files.append(file)     
                self.file_handler.exclude(file)

        # Added this here for TESTING
        return receipts, excluded_files

    def name_check(self,file):

        pattern = re.compile(r'(lidl_receipt)(\d+)\.(jpg|jpeg|png)',re.IGNORECASE)
        all_processed = os.listdir(self.accepted_dir)
        all_processed.sort(reverse=True)
        last_receipt = all_processed[0]
        match = re.search(pattern,last_receipt)

        extension_pattern = re.compile(r'(.+)(jpg|jpeg|png)$')
        file_extension = re.search(extension_pattern,file)
        
        if match:
            print(f"{match.group(2)} was the last receipt inserted")
            print(f"lidl_receipt{int(match.group(2))+1}{file_extension.group(2)}")
        else:
            return 0

    # Checks whether the file can be opened
    def open_photo_check(self,file,dir):
        try:
            Image.open(os.path.join(dir,file))
            self.logger.log_message(f"File {file} passed image opening test")
            return True
        except:
            self.logger.log_message(f"File {file} failed image opening test")
        return False

    # Chceks whether the file has the right extension for a photo
    def file_extension_check(self,file):

        right_extension = self.extension_check.search(file)

        if right_extension:
            self.logger.log_message(f"File {file} passed extension test")
            return True
        else:
            self.logger.log_message(f"File {file} failed extension test")
            return False

    # Reads the receipt provided to the file
    def read_receipt(self,receipt):
    
        file_path=os.path.dirname(__file__)
        relative_path="..\\Receipts\\" + receipt
        path=file_path+"\\"+relative_path

        pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'
        image = cv2.imread(path)

        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Threshold to make text stand out
        _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        # Optional: remove noise
        denoised = cv2.medianBlur(thresh, 3)
    
        text = pytesseract.image_to_string(denoised,lang='eng')
        lines = [line for line in text.splitlines() if line.strip()]
        
        json_receipt = self.extract_items(lines)

        return json_receipt

    # Compiles the regex that will be used when extracting items
    def compile_regex(self):
        self.extension_check = re.compile(r'(.+)\.(jpg|jpeg|png)',re.IGNORECASE)
        self.time_search = re.compile(r"(Time:\s+)(\d{2}:\d{2}:\d{2})")
        self.date_search = re.compile(r"(Date:\s+)(\d{2}\/\d{2}\/\d{2})")
        self.item_search = re.compile(r"(.*\s)(-?\d{1,3}\.\d{2})")
        self.total_search = re.compile(r"(TOTAL)(\s+)(\d{1,4}\.\d{2})")
        self.payment_search = re.compile(r"CARD", re.IGNORECASE)
        self.discount_search = re.compile(r"(TOTAL DISCOUNT\s*)(\d{1,2}.\d{1,2})")
        self.quantity_check = re.compile(r"(\d{1,2})(\s?[xX]{1,2}\s*£\d{1,2}.\d{1,2})")
        self.weight_check = re.compile(r"(\d{1,2}\.\d{1,3})(\s?kg\s?@\s?£\s?)(\d{1,2}\.\d{1,2})")

    # Extracts the items from the receipt text
    def extract_items(self,text):

        receipt_dict = {}
        items = []
        items_dict = {}

        for i, line in enumerate(text):
               
               # Looks for any reference to price / cost
               match = self.item_search.search(line)

               if match:

                   # Looking for payment information to skip
                   payment = self.payment_search.search(match.group())

                   # Retrieves the total cost on the receipt
                   total_cost = self.total_search.search(match.group())

                   # Retrieves the total discount on the receipt
                   total_discount = self.discount_search.search(match.group())
                   
                   if total_discount:
                       receipt_dict.update({"discount":f"{total_discount.group(2)}"})
                       break
                   
                   elif total_cost:
                       receipt_dict.update({"total":f"{total_cost.group(3)}"})

                   elif not payment and not total_cost:
                       
                       quantity_check = self.quantity_check.search(line)
                       
                       weight_check_next = self.weight_check.search(text[i+1])
                       
                       weight_check_current = self.weight_check.search(line)

                       # Checks whether there is a quantity given for the item bought
                       if quantity_check:
                           price = float(match.group(2)) / int(quantity_check.group(1))
                           items.append({"name":f"{match.group(1).replace(quantity_check.group(),"")}".strip(),
                                         "price":f"{price}","quantity":f"{quantity_check.group(1)}"})
                        
                       # Checks whether there is a weight given for the item bought
                       elif weight_check_next:
                           weight_bought = float(weight_check_next.group(1))
                           items.append({"name":f"{match.group(1)}".strip(),
                                         "price":f"{match.group(2)}",
                                         "weight":f"{weight_bought}",
                                         "ppkg":f"{weight_check_next.group(3)}"})
                        
                       # Checks whether the current item is just a weight, in which case skip
                       elif weight_check_current:
                           continue
                       
                       # In general, add the name and price only
                       else:
                           items.append({"name":f"{match.group(1)}".strip(),
                                         "price":f"{match.group(2)}"})
                   else:
                       continue

               # Looks for the date on the receipt 
               date = self.date_search.search(line)
               
               if date:
                   receipt_dict.update({"date":f"{date.group(2)}"})

               # Looks for the time on the receipt 
               time = self.time_search.search(line)

               if time:
                   receipt_dict.update({"time":f"{time.group(2)}"})

               # Looks for the total on the receipt
               total_cost = self.total_search.search(line)

               if total_cost:
                   receipt_dict.update({"total":f"{total_cost.group(3)}"})

        # Constructs the dictionary for the receipt
        items_dict.update({"items":items})
        receipt_dict.update(items_dict)

        # (For testing purposes only) Prints out the dictionary in JSON format
        json_receipt_nice = json.dumps(receipt_dict,indent=4,ensure_ascii=False).encode("utf-8")
        #print(json_receipt_nice.decode())

        # Adds the receipt to the list of the receipts to be processed
        json_receipt = json.dumps(receipt_dict)
        self.receipts.append(json_receipt)

        return json_receipt


if __name__ == '__main__':

    """
    #reading = sys.stdin.readline().strip()
    #print(f"Python got: {reading}")
    for receipt in reader.receipts:
        sys.stdout.writelines(receipt + "\n")
        sys.stdout.flush()

    sys.stdout.close()
    """
               
