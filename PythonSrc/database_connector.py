import pyodbc
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

    def __exit__(self,exception_type,exception_value,exception_traceback): 
        self.connection.close()

if __name__ == '__main__':
    with DatabaseConnector() as dbc:
         dbc.callP()
         #print(datetime.now().year)

