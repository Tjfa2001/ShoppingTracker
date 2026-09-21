"Module docstring"
from app_context import create_app_context
from ShoppingTracker.PythonSrc.core.housekeep import archive_old_log_files
from ShoppingTracker import process_receipt


def main():
    """Main function to run the shopping tracker application"""

    ctx = create_app_context()

    # Running housekeeping on log directory to remove files older than 30 days
    archive_old_log_files()

    # Retrieving receipts from Receipts directory
    valid_receipts, _excluded_receipts = ctx.reader.get_receipts()

    if not valid_receipts:
        ctx.logger.log_message("No files to process... Exiting")
    else:
        ctx.logger.log_message("Files to process!")
        for receipt in valid_receipts:
            process_receipt(receipt = receipt, context = ctx)

    ctx.logger.write_to_file()

# This module is intended to be run directly
if __name__ == '__main__':
    main()
