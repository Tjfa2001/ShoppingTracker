import os

pythonSource = os.path.dirname(__file__)
projectDirectory = os.path.dirname(pythonSource)
dictionaryLocation = os.path.join(pythonSource,"CategoryDict.json")

# Master Dictionary Locations
masterDictionaryLocation = os.path.join(projectDirectory,"MasterDictionary\MastDict.json")

# Categories Locations
categoriesDictFile = os.path.join(pythonSource,"Categories\CategoryDict.json")
categoryFilePath = os.path.join(pythonSource,"categories.txt")

# Receipt Directories
acceptedReceiptsDirectory = os.path.join(projectDirectory,"Accepted")
excludedReceiptsDirectory = os.path.join(projectDirectory,"Excluded")
processedReceiptsDirectory = os.path.join(projectDirectory,"ProcessedReceipts")
receiptsDirectory = os.path.join(projectDirectory,"Receipts")

# Logger Variable
logDirectory = os.path.join(projectDirectory,"Logs")

# Database Variables
databaseConnectionString = """Driver={PostgreSQL UNICODE};
                              Server=localhost;
                              Port=5432;
                              Database=lidl_receipts;
                              Uid=postgres;
                              Pwd=postgres;"""
                              
# Data Displayer Settings
geometry = '2000x1000'
dataDisplayerTitle = 'Toms Data Displayer'

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