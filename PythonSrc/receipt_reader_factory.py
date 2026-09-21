"""
Factory class to return the correct receipt reader based
on the shop that the receipt is from
"""


from ShoppingTracker.PythonSrc.ReceiptReaders.base import ReceiptReader
from ShoppingTracker.PythonSrc.ReceiptReaders.lidl_receipt_reader import LidlReceiptReader as LidlRR

class ReceiptReaderFactory():
    """Factory to make a receipt reader"""

    @staticmethod
    def create_receipt_reader(shop:str, logger) -> ReceiptReader:
        """a"""

        if shop == "Lidl":
            return LidlRR(logger)
        return LidlRR(logger)
