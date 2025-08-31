import pyodbc

class DatabaseConnector():

    def __init__(self):
        connection = pyodbc.connect('Driver={PostgreSQL UNICODE};Server=localhost;Port=5432;Database=lidl_receipts;Uid=postgres;Pwd=postgres;')
        cur = connection.cursor()
        cur.execute("SELECT * FROM lidl.receipts;")
        all = cur.fetchall()
        cur.commit()
        for row in all:
            print(row)
        connection.close()
        print("HELLO")

DatabaseConnector()