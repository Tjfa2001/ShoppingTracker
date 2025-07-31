import pytesseract
import cv2
from PIL import Image
import os

if __name__ == '__main__':
    print("Test")
    
    file_path=os.path.dirname(__file__)
    relative_path="Receipts\\receipt2.jpg"
    path=file_path+"\\"+relative_path
    pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'
    Image.open(path).show()
    image = cv2.imread(path)

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Threshold to make text stand out
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Optional: remove noise
    denoised = cv2.medianBlur(thresh, 3)

    print(pytesseract.image_to_string(Image.open(path),lang='eng'))
    print(pytesseract.image_to_string(denoised,lang='eng'))