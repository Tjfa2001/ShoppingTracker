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