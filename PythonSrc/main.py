import receipt_reader as rr
import my_logger as logger
import file_handler as fh
import validator as val

def main():
    reader = rr.ReceiptReader()
    valid_receipts, excluded = reader.get_receipts()
    file_handler = fh.FileHandler()
    validator = val.Validator()

    if valid_receipts is None:
        reader.logger.log_message("No files to process... Exiting")
    else:
        reader.logger.log_message("Files to process:")
        for receipt in valid_receipts:
            #if receipt == 'lidl_receipt1.png':
                text = reader.read_receipt(receipt)
                json_receipt = reader.extract_items(text)
                validator.validate_receipt(receipt,json_receipt)

if __name__ == '__main__':
    main()