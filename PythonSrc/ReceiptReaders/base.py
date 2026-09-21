from abc import ABC, abstractmethod

class ReceiptReader(ABC):
    "Interface for receipt readers"

    @abstractmethod
    def log(self, message:str) -> None:
        """Log a message"""

    @abstractmethod
    def get_receipts(self) -> list[str]:
        """Get any receipts for the selected store"""
