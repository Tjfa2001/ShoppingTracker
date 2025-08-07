import pytesseract
import cv2
from PIL import Image
import os
import re
import logger

def get_receipts():

    abspath = os.path.abspath(".")
    receipt_dir = os.path.join(abspath,r"ShoppingTracker\Receipts")

    receipts = []
    excluded_files = []

    for file in os.listdir(receipt_dir):
        pass_extension_check = file_extension_check(file)
        pass_openable_photo_check = open_photo_check(file,receipt_dir)

        if pass_extension_check and pass_openable_photo_check:
            receipts.append(file)
        else:
            excluded_files.append(file)

    return receipts, excluded_files

def open_photo_check(file,dir):
    try:
        Image.open(os.path.join(dir,file))
        logger.log_message(f"File {file} passed image opening test")
        return True
    except:
        logger.log_message(f"File {file} failed image opening test")
        return False

def file_extension_check(receipt):
    match = re.search(r'(.+)\.(jpg|jpeg|png)',receipt,re.IGNORECASE)
    if match:
        file_name = match.group()
        logger.log_message(f"File {file_name} passed extension test")
        return True
    else:
        logger.log_message(f"File {receipt} failed extension test")
        return False

def read_receipt(receipt):
    
    file_path=os.path.dirname(__file__)
    relative_path="Receipts\\receipt2.jpg"
    path=file_path+"\\"+relative_path
    pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'
    #Image.open(path).show()
    image = cv2.imread(path)

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Threshold to make text stand out
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Optional: remove noise
    denoised = cv2.medianBlur(thresh, 3)

    #print(pytesseract.image_to_string(Image.open(path),lang='eng'))
    text = pytesseract.image_to_string(denoised,lang='eng')
    #print(pytesseract.image_to_string(denoised,lang='eng'))
    return text

if __name__ == '__main__':
    receipts, excluded = get_receipts()

    if receipts is None:
        logger.log_message("No files to process... Exiting")
    else:
        logger.log_message("Files to process:")
        for receipt in receipts:
            print(receipt)
            text = read_receipt(receipt)
