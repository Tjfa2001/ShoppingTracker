"""Process a single receipt"""

from core import AppContext

def process_receipt(receipt: str,
                    ctx: AppContext):

    """Processes a single receipt"""
    ctx.logger.log_message(f"Reading receipt: {receipt}")
    json_receipt = ctx.reader.read_receipt(receipt)

    ctx.logger.log_message(f"Validating receipt: {receipt}")
    validated_receipt = ctx.validator.validate_receipt(json_receipt)

    if not validated_receipt:
        ctx.logger.log_message("Receipt was not validated")
        ctx.file_handler.exclude(receipt)
    else:
        ctx.logger.log_message("Receipt was successfully validated")
        ctx.file_handler.write_json_receipt_to_file(receipt,validated_receipt)
        ctx.db_connect.send_to_database(receipt,validated_receipt)
        ctx.file_handler.accept(receipt)
