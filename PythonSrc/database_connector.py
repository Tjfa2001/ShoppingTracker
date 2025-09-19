import pyodbc
import re
from datetime import date, time, datetime

class DatabaseConnector():

    connection = None

    def __init__(self):
        self.connection = pyodbc.connect("""Driver={PostgreSQL UNICODE};
                                            Server=localhost;
                                            Port=5432;
                                            Database=lidl_receipts;
                                            Uid=postgres;
                                            Pwd=postgres;""")
    def __enter__(self):
        
        self.connection.setencoding(encoding='utf-8')
        self.connection.setdecoding(pyodbc.SQL_CHAR,encoding='utf-8')
        self.connection.setdecoding(pyodbc.SQL_WCHAR,encoding='utf-8')
        return self

    def executeSQL(self,SQL):
        cur = self.connection.cursor()
        cur.execute("SELECT * FROM lidl.receipts WHERE total > ? AND discount <= ?;",(1,5))
        all = cur.fetchall()
        #cur.commit()
        for row in all:
            print(row.receipt)

    def callP(self):
        cur = self.connection.cursor()
        try:
            p_date = date(2025,9,14)
            p_now = datetime.now()
            p_time = f"{p_now.hour}:{p_now.minute}:"
            cur.execute('CALL insert_receipt(?,?,?,?,?);',("test_receipt4.jpg",10,0,p_date,p_time))
            self.executeSQL("b")
        except pyodbc.DatabaseError as err:
            cur.rollback()
            print(err.args[1])
        finally:
            cur.commit()

    def send_to_database(self,receipt_name,validated_receipt):
        items=validated_receipt['items']
        total=validated_receipt['total']
        discount=validated_receipt['discount']
        date_from_r=validated_receipt['date']

        date_pattern = re.compile(r'(\d+)/(\d+)/(\d+)')
        match = re.search(date_pattern,date_from_r)

        if match:
            year = f"20{match.group(3)}"
            month = match.group(2)
            day = match.group(1)
            iso_date = f"{year}-{month}-{day}"
        else:
            iso_date = "2001-09-17"

        correct_date = date.fromisoformat(iso_date)
        time=validated_receipt['time']

        for item in items:
            name = item['name']

            if "ppkg" in item:
                price = item['ppkg']
            else:
                price = item['price']
            
            if "quantity" in item:
                quantity = item['quantity']
            else:
                quantity = 1
            
            cost = int(quantity) * float(price)

            self.send_to_item_table(receipt_name,name,price,quantity,cost)

        self.send_to_receipt_table(receipt_name,total,discount,correct_date,time)

    def send_to_item_table(self,receipt,item,price,quantity,cost):
        cur = self.connection.cursor()
        try:
            cur.execute('CALL lidl.insert_item(?,?,?,?,?);',(receipt,item,price,quantity,cost))
        except pyodbc.DatabaseError as err:
            cur.rollback()
            print(err.args[1])
            print(err)
        finally:
            cur.commit()

    def send_to_receipt_table(self,receipt,total,discount,date,time):
        cur = self.connection.cursor()
        try:
            cur.execute('CALL lidl.insert_receipt(?,?,?,?,?);',(receipt,total,discount,date,time))
        except pyodbc.DatabaseError as err:
            cur.rollback()
            print(err.args[1])
        finally:
            cur.commit()

    def __exit__(self,exception_type,exception_value,exception_traceback): 
        self.connection.close()

if __name__ == '__main__':
    with DatabaseConnector() as dbc:
         #dbc.callP()
        test_date = '22/06/25'
        date_pattern = re.compile(r'(\d+)/(\d+)/(\d+)')
        match = re.search(date_pattern,test_date)
        if match:
            year = f"20{match.group(3)}"
            month = match.group(2)
            day = match.group(1)
            iso_date = f"{year}-{month}-{day}"

        d = date.fromisoformat(iso_date)    
        
         
         

