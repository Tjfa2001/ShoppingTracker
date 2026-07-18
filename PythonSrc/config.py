"""Configuration variables for the project"""

import os

PYTHON_SRC = os.path.dirname(__file__)
PROJ_DIR = os.path.dirname(PYTHON_SRC)
DICT_LOC = os.path.join(PYTHON_SRC,"CategoryDict.json")

# Master Dictionary Locations
MAST_DICT_LOC = os.path.join(PROJ_DIR,r"MasterDictionary\MastDict.json")

# Categories Locations
CATEGORY_DICT_FILE = os.path.join(PYTHON_SRC,r"Categories\CategoryDict.json")
CATEGORY_FILE_LOC = os.path.join(PYTHON_SRC,"categories.txt")

# Receipt Directories
ACC_RECEIPT_DIR = os.path.join(PROJ_DIR,"Accepted")
EXCL_RECEIPT_DIR = os.path.join(PROJ_DIR,"Excluded")
PROC_RECEIPT_DIR = os.path.join(PROJ_DIR,"ProcessedReceipts")
INPUT_RECEIPT_DIR = os.path.join(PROJ_DIR,"Receipts")

# Logger Variable
LOG_DIR = os.path.join(PROJ_DIR,"Logs")
LOG_ARCHIVE_DIR = os.path.join(LOG_DIR,"Archive")

# Database Variables
DB_CONN_STR = """Driver={PostgreSQL UNICODE};
                 Server=localhost;
                 Port=5432;
                 Database=lidl_receipts;
                 Uid=postgres;
                 Pwd=postgres;"""

# Data Displayer Settings
DATA_DISPLAYER_GEOMETRY = '2000x1000'
DATA_DISPLAYER_TITLE = 'Toms Data Displayer'

MONTHLY_DATA_SQL = """
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
