import pandas as pd
import database_connector as dbc
import my_logger as logger
import file_handler as fh

if __name__ == '__main__':
    
    file_h = fh.FileHandler()
    logger_t = logger.Logger(file_h)
    connector = dbc.DatabaseConnector(logger_t)
    dataframe = pd.read_sql("SELECT * FROM lidl.items;",con=connector.connection)
    print(dataframe)