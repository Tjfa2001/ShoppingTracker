"""
Classes
~~~~~~~~~~~~~
AppContext - Dataclass to store context objects for application

Functions
~~~~~~~~~~~~~
create_app_context - Returns an application context
"""

from dataclasses import dataclass

import sys
import os

# Add PythonSrc to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from my_logger import Logger
from database_connector import DatabaseConnector
from file_handler import FileHandler
from validator import Validator
import receipt_reader_factory as rrf
from ReceiptReaders.base import ReceiptReader
# PythonSrc/Core/FileB.py

@dataclass
class AppContext:

    """App context for the receipt reader project"""
    receipt_reader: ReceiptReader
    file_handler: FileHandler
    database_connector: DatabaseConnector
    validator: Validator
    logger: Logger

def create_app_context():
    """Creates the app context to read receipts"""

    # Create file handling class and logging class
    file_handler = FileHandler()
    logger = Logger(file_handler,debug=True)
    file_handler.logger = logger
    logger.log_message("File handler and logger created")

    # Creating receipt reader object
    reader = rrf.ReceiptReaderFactory.create_receipt_reader(shop="Lidl", logger=logger)

    # Creates validator to validate receipts
    validator = Validator(logger)

    # Creates a database connector
    db_connect = DatabaseConnector(logger)

    context = AppContext(
        receipt_reader=reader,
        file_handler=file_handler,
        database_connector=db_connect,
        validator=validator,
        logger=logger)

    return context
