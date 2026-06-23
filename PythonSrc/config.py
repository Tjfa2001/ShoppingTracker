import os

PYTHON_SOURCE = os.path.dirname(__file__)
PROJECT_DIRECTORY = os.path.dirname(PYTHON_SOURCE)
DICT_LOCATION = os.path.join(PYTHON_SOURCE,"CategoryDict.json")

# Master Dictionary Locations
MAST_DICT_LOCATION = os.path.join(PROJECT_DIRECTORY,"MasterDictionary\MastDict.json")

# Categories Locations
CATEGORY_DICT_FILE = os.path.join(PYTHON_SOURCE,"Categories\CategoryDict.json")
CATEGORY_FILE_PATH = os.path.join(PYTHON_SOURCE,"categories.txt")

# Receipt Directories
ACCEPTED_RECEIPTS_DIR = os.path.join(PROJECT_DIRECTORY,"Accepted")
EXCLUDED_RECEIPTS_DIR = os.path.join(PROJECT_DIRECTORY,"Excluded")
PROCESSED_RECEIPTS_DIR = os.path.join(PROJECT_DIRECTORY,"ProcessedReceipts")
RECEIPTS_DIRECTORY = os.path.join(PROJECT_DIRECTORY,"Receipts")

# Logger Variable
LOG_DIRECTORY = os.path.join(PROJECT_DIRECTORY,"Logs")
LOG_ARCHIVE_DIR = os.path.join(LOG_DIRECTORY,"Archive")

# Database Variables
DB_CONNECTION_STR = """Driver={PostgreSQL UNICODE};
                              Server=localhost;
                              Port=5432;
                              Database=lidl_receipts;
                              Uid=postgres;
                              Pwd=postgres;"""
                              
# Data Displayer Settings
DATA_DISPLAY_MAX_DIM = '2000x1250'
DATA_DISPLAY_MIN_DIM = '500x500'
DATA_DISPLAY_TITLE = 'Toms Data Displayer'

monthSQL = """
    SELECT
    i.category,
    date_part('month',r.date) as month,
    date_part('year',r.date) as year,
    sum(i.cost) as total_cost
    FROM
    lidl.items i
    LEFT JOIN
    lidl.receipts r
    ON i.receipt = r.receipt
    GROUP BY
    date_part('month',r.date),
    date_part('year',r.date), i.category;
    """