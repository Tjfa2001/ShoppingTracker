import pyodbc
import re
import config
import json
from datetime import date, time, datetime

class DatabaseConnector():

    connection = None
    date_pattern = None
    logger = None

    def __init__(self,logger):
        # Connect to your postgres DB
        self.connection = pyodbc.connect(config.databaseConnectionString)
        if logger:
            self.logger = logger
        self.log("Database connection established")
        self.compile_regex()

    def __enter__(self):
        # Set encoding for the connection
        self.connection.setencoding(encoding='utf-8')
        self.connection.setdecoding(pyodbc.SQL_CHAR,encoding='utf-8')
        self.connection.setdecoding(pyodbc.SQL_WCHAR,encoding='utf-8')
        return self

    def log(self,message: str):
        if self.logger:
            self.logger.log_message(message)
            return True
        else:
            return False
        
    def log_error(self,error_msg):
        if self.logger:
            self.logger.log_error(error_msg)
            return True
        else:
            return False

    def send_to_database(self,receipt_name,validated_receipt):
        # Send validated receipt data to the database
        items=validated_receipt['items']
        total=validated_receipt['total']
        
        if 'discount' not in validated_receipt:
            discount = 0
        else:
            discount=validated_receipt['discount']

        date_from_receipt=validated_receipt['date']
        correct_date = date.fromisoformat(self.format_date_for_db(self.date_pattern.search(date_from_receipt)))

        time=validated_receipt['time']

        for item in items:
            name, price, quantity, cost = self.extract_item_info(item)
            self.send_to_item_table(receipt_name,name,price,quantity,cost)
            self.log(f"Processing item: {name}")
            
            with open(config.categoriesDictFile,"r") as category_dict:
                category_dict = json.loads(category_dict.read())
                if name in category_dict:
                    category = category_dict[f"{name}"]
                    self.log(f"Found category {category} for item: {name}")
                else:
                    self.log(f"No category found for item: {name}")
                    category = ""
                
            self.update_category(item_name=name,category=category)

        self.send_to_receipt_table(receipt_name,total,discount,correct_date,time)

    # Extracts item information from an item JSON object
    def extract_item_info(self,item):
        name = item['name']

        # If there is a price per kilogram, extract this, otherwise extract the price
        if "ppkg" in item:
            price = item['ppkg']
        else:
            price = item['price']
        
        # If there is a quantity, extract this, otherwise set to 1
        if "quantity" in item:
            quantity = item['quantity']
        else:
            quantity = 1
        
        # Multiply the quantity by the price to get the total cost for that item
        cost = int(quantity) * float(price)
        
        return name, price, quantity, cost

    def format_date_for_db(self,match):
        # Format date to ISO format for database
        if match:
            year = f"20{match.group(3)}"
            month = match.group(2)
            day = match.group(1)
            iso_date = f"{year}-{month}-{day}"
        else:
            iso_date = "2001-09-17"
            
        return iso_date
    
    def send_to_item_table(self,receipt,item,price,quantity,cost):
        self.log(f"Sending item {item} to database")
        cur = self.connection.cursor()
        try:
            cur.execute('CALL lidl.insert_item(?,?,?,?,?);',(receipt,item,price,quantity,cost))
        except pyodbc.DatabaseError as err:
            cur.rollback()
            self.log_error(err.args[1])
        finally:
            cur.commit()

    def send_to_receipt_table(self,receipt,total,discount,date,time):
        self.log(f"Sending receipt {receipt} to database")
        cur = self.connection.cursor()
        try:
            cur.execute('CALL lidl.insert_receipt(?,?,?,?,?);',(receipt,total,discount,date,time))
        except pyodbc.DatabaseError as err:
            cur.rollback()
            self.log_error(err.args[1])
        finally:
            cur.commit()
            
    def compile_regex(self):
        self.date_pattern = re.compile(r'(\d+)/(\d+)/(\d+)')

    def update_category(self,item_name,category):
        cur = self.connection.cursor()
        try:
            cur.execute('CALL lidl.update_category(?,?);',(item_name,category))
        except pyodbc.DatabaseError as err:
            cur.rollback()
            self.log_error(err.args[1])
        finally:
            cur.commit()
        
    def __exit__(self,exception_type,exception_value,exception_traceback): 
        # Close the database connection
        self.connection.close()

if __name__ == '__main__':
    with DatabaseConnector() as dbc:
        test_date = '22/06/25'
        date_pattern = re.compile(r'(\d+)/(\d+)/(\d+)')
        match = re.search(date_pattern,test_date)
        if match:
            year = f"20{match.group(3)}"
            month = match.group(2)
            day = match.group(1)
            iso_date = f"{year}-{month}-{day}"

        d = date.fromisoformat(iso_date)    