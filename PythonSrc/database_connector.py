"""DatabaseConnector class"""
import re
import json
from datetime import date
import core.config as config
import pyodbc

class DatabaseConnector():

    """Object to connect to a database for SQL transactions"""

    connection = None
    date_pattern = None

    logger = None

    def __init__(self,logger):
        # Connect to your postgres DB
        self.connection = pyodbc.connect(config.DB_CONN_STR)
        if logger:
            self.logger = logger
        self.log("Database connection established")
        self.compile_all_regex()

    def __enter__(self):
        # Set encoding for the connection
        self.connection.setencoding(encoding='utf-8')
        self.connection.setdecoding(pyodbc.SQL_CHAR,encoding='utf-8')
        self.connection.setdecoding(pyodbc.SQL_WCHAR,encoding='utf-8')
        return self

    def log(self, message: str):
        """Log a message via the Logger class"""
        if self.logger:
            self.logger.log_message(message)
            return True
        return False

    def log_error(self,error_msg):
        """Log an error message via the Logger class"""
        if self.logger:
            self.logger.log_error(error_msg)
            return True
        return False

    def send_to_database(self,receipt_name,validated_receipt):
        """Send validated receipt data to the database"""
        items=validated_receipt['items']
        total=validated_receipt['total']

        if 'discount' not in validated_receipt:
            discount = 0
        else:
            discount=validated_receipt['discount']

        date_from_receipt=validated_receipt['date']
        correct_date = date.fromisoformat(
            self.format_date_for_db(self.date_pattern.search(date_from_receipt))
        )

        for item in items:
            name, price, quantity, cost = self.extract_item_info(item)
            self.send_to_item_table(receipt_name,name,price,quantity,cost)
            self.log(f"Processing item: {name}")

            with open(config.CATEGORY_DICT_FILE,"r",encoding="utf-8") as category_dict:
                category_dict = json.loads(category_dict.read())
                if name in category_dict:
                    category = category_dict[f"{name}"]
                    self.log(f"Found category {category} for item: {name}")
                else:
                    self.log(f"No category found for item: {name}")
                    category = ""

            self.update_category_for_item(item_name=name,category=category)

        self.send_to_receipt_table(receipt_name,total,discount,correct_date,time)

    def extract_item_info(self,item):
        """Extracts item information from an item JSON object"""
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
        """Format date to ISO format for database"""
        iso_date = "2001-09-01"
        if match:
            year = f"20{match.group(3)}"
            month = match.group(2)
            day = match.group(1)
            iso_date = f"{year}-{month}-{day}"
        else:
            self.log_error("Unable to format date in DatabaseConnector")

        return iso_date

    def send_to_item_table(self,receipt,item,price,quantity,cost):
        """Send an item to the Postgres database table with its related information"""
        self.log(f"Sending item {item} to database")
        cur = self.connection.cursor()
        try:
            cur.execute(config.INSERT_ITEM_INTO_DB_SQL,(receipt,item,price,quantity,cost))
        except pyodbc.DatabaseError as err:
            cur.rollback()
            self.log_error(f"Error sending {item} to the database: {err.args[1]}")
        finally:
            cur.commit()

    def send_to_receipt_table(self,receipt,total,discount,receipt_date,receipt_time):
        """Send a receipt to the Postgres database table with its related information"""
        self.log(f"Sending receipt {receipt} to database")
        cur = self.connection.cursor()
        try:
            cur.execute(
                config.INSERT_RECEIPT_INTO_DB_SQL,
                (receipt,total,discount,receipt_date,receipt_time)
            )
        except pyodbc.DatabaseError as err:
            cur.rollback()
            self.log_error(f"Error sending {receipt} to the database: {err.args[1]}")
        finally:
            cur.commit()

    def compile_all_regex(self):
        """Compiles all regex for the DatabaseConnector class"""
        self.date_pattern = re.compile(r'(\d+)/(\d+)/(\d+)')

    def update_category_for_item(self,item_name,category):
        """Update the category for an item"""
        cur = self.connection.cursor()
        try:
            cur.execute(config.UPDATE_CATEGORY_SQL,(item_name,category))
        except pyodbc.DatabaseError as err:
            cur.rollback()
            self.log_error(err.args[1])
        finally:
            cur.commit()

    def __exit__(self,exception_type,exception_value,exception_traceback):
        # Close the database connection
        self.connection.close()

if __name__ == '__main__':
    print("This module is not meant to be run directly")
