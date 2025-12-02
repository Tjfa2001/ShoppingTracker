import pandas as pd
import database_connector as dbc
import my_logger as logger
import file_handler as fh
import data_displayer as dd

if __name__ == '__main__':
    
    

    file_h = fh.FileHandler()
    logger_t = logger.Logger(file_h)
    connector = dbc.DatabaseConnector(logger_t)
    data_disp = dd.DataDisplayer(connector)
    
    #data_disp.conn = connector
    """
    dataframe = pd.read_sql("SELECT * FROM lidl.items;",con=connector.connection)
    printing = dataframe.sort_values("item", ascending=True)
    printing = printing.assign(total_c=(printing["price"]*printing["quantity"]))
    print(printing[printing["quantity"]>1])"""