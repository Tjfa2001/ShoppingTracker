import receipt_reader as rr
import my_logger as l
import file_handler as fh
import validator as val
import database_connector as dc
from datetime import date

# Main function to run the shopping tracker application
def main():

    # Create instances of necessary classes
    file_handler = fh.FileHandler()
    logger = l.Logger(file_handler)
    logger.log_message("File handler and logger created")
    reader = rr.ReceiptReader(logger)
    logger.log_message("Retrieving receipts")
    valid_receipts, excluded = reader.get_receipts()
    validator = val.Validator(logger)
    db_connect = dc.DatabaseConnector(logger)

    if valid_receipts is None:
        logger.log_message("No files to process... Exiting")
    else:
        #logger.log_message("Files to process:")

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


if __name__ == '__main__':
    main()
    