import receipt_reader as rr
import my_logger as l
import file_handler as fh
import validator as val
import database_connector as dc
import subprocess
import config as cf
import os
from datetime import date

# Main function to run the shopping tracker application
def main():

    # Create file handling class and logging class
    file_handler = fh.FileHandler()
    logger = l.Logger(file_handler,debug=True)
    file_handler.logger = logger
    logger.log_message("File handler and logger created")
    
    # Running housekeeping on log directory to remove files older than 30 days
    housekeep = os.path.join(cf.pythonSource,'housekeep.py')
    completed_subprocess = subprocess.run(['python',housekeep],capture_output=True)
    housekeep_log = completed_subprocess.stdout.decode().splitlines()  
    logger.log_list_log(housekeep_log)
    
    # Creating receipt reader object
    reader = rr.ReceiptReader(logger)
    logger.log_message("Retrieving receipts")
    
    # Retrieving receipts from Receipts directory
    valid_receipts, excluded = reader.get_receipts()
    
    # Creates validator to validate receipts
    validator = val.Validator(logger)
    
    # Creates a database connector
    db_connect = dc.DatabaseConnector(logger)
    
    if not valid_receipts:
        logger.log_message("No files to process... Exiting")
    else:
        logger.log_message("Files to process!")
        for receipt in valid_receipts:
                
                logger.log_message(f"Reading receipt: {receipt}")
                json_receipt = reader.read_receipt(receipt)
            
                logger.log_message(f"Validating receipt: {receipt}")
                validated_receipt = validator.validate_receipt(json_receipt)

                if not validated_receipt:
                    logger.log_message(f"Receipt was not validated")
                    file_handler.exclude(receipt) 
                else:
                    logger.log_message(f"Receipt was successfully validated")
                    file_handler.write_json_receipt_to_file(receipt,validated_receipt)
                    db_connect.send_to_database(receipt,validated_receipt)
                    file_handler.accept(receipt)

    logger.write_to_file()

# This module is intended to be run directly
if __name__ == '__main__':
    main()