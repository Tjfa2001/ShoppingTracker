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
                json_receipt = reader.read_receipt(receipt)

                validated_receipt = validator.validate_receipt(json_receipt)

                if not validated_receipt:
                    file_handler.exclude(receipt) 
                else:
                    file_handler.write_json_receipt_to_file(receipt,validated_receipt)
                    file_handler.accept(receipt)

if __name__ == '__main__':
    main()