import pandas as pd
import database_connector as dbc
import my_logger as logger
import file_handler as fh
import data_displayer as dd
import pandas as pd
import config as cf
import sqlalchemy as sqa
import psycopg2
import datetime as dt
import matplotlib.pyplot as plt

if __name__ == '__main__':

    file_h = fh.FileHandler()
    logger_t = logger.Logger(file_h)
    connector = dbc.DatabaseConnector(logger_t)
    
    engine = sqa.create_engine("postgresql://postgres:postgres@localhost/lidl_receipts")
    connect = engine.connect()
    
    sql_statement1 = """
    SELECT
    i.*,
    r.date
    FROM
    lidl.items i
    INNER JOIN
    lidl.receipts r
    ON 
    i.receipt = r.receipt;
    """
    
    # You can uncomment this to get the GUI to pop up
    data_disp = dd.DataDisplayer(connect,sql=cf.monthSQL)
    """
    df = pd.read_csv('dataframe_with_dates.csv')
    df['date'] = pd.to_datetime(df['date'])
    df['month'] = df['date'].dt.strftime('%b')
    df['year'] = df['date'].dt.strftime('%Y')
    
    df = df[['month','year','cost']]
    df = df.groupby(by=['month','year']).sum()
    
    df.to_csv('dataframe_by_months.csv')
    """
    
    #
    # Me playing around to display spend by month in matplotlib
    #
    """
    df = pd.read_csv('dataframe_by_months.csv')
    df['month_year'] = pd.to_datetime(df['year'].astype(str)+'-'+df['month'].astype(str)).dt.strftime('%b-%Y')
    df['month'] = pd.to_datetime('2025-' + df['month'].astype(str)).dt.strftime('%m')
    df = df.sort_values(by=['year','month'])
    print(df)
    df.plot(x='month_year', y='cost', kind='bar', title='Monthly Costs')
    plt.ylabel('Cost (£)')
    plt.xlabel('Month')
    plt.show()
    
    print("PLOTTED")
    """
    
    """
    dataframe = pd.read_sql("SELECT * FROM lidl.items;",con=connector.connection)
    printing = dataframe.sort_values("item", ascending=True)
    printing = printing.assign(total_c=(printing["price"]*printing["quantity"]))
    print(printing[printing["quantity"]>1])"""