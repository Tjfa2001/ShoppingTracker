import os
import json
import re
import config
from datetime import datetime

class FileHandler():
    """
    
    Class that handles file operations for the Shopping Tracker project, including
    logging, moving receipts into the correct directories and renaming files.
    
    """
    
    logger = None

    def __init__(self,
        processed_directory: str | None = None,
        receipt_directory: str | None = None,
        accepted_directory: str | None = None,
        excluded_directory: str | None = None,
        log_directory: str | None = None):
        
        """
        Creates an instance of the file handler class.
        
        Args:
            processed_directory: Destination for processed receipt data.
            receipt_directory: Source directory for incoming receipts.
            accepted_directory: Storage for approved receipt images.
            excluded_directory: Storage for rejected receipts.
            log_directory: Location for log files.
            
        """
        self.processed_directory = processed_directory
        self.receipt_directory = receipt_directory
        self.accepted_directory = accepted_directory
        self.excluded_directory = excluded_directory
        self.log_directory = log_directory
        self.get_directories()
        self.compile_regex()

    def compile_regex(self):
        """Compiles the regex used by the file handler"""
        self.filename_search = re.compile(r"(\w+)\.(\w+)")

    def write_logger_to_file(self,logger):
        """
        Writes a Logger object to a log file
        
        Args:
            logger (Logger): The logger object to be written to a file
        
        Returns:
            nothing
        """
        
        timestamp = datetime.now().strftime("%d%m%Y_%H%M%S")
        log_name = f"log_{timestamp}"
        
        try:
            os.makedirs(self.log_directory, exist_ok=True)
        except OSError:
            self.log("File Handler unable to make directory")
        
        with open(os.path.join(self.log_directory,log_name),'w') as file:
            for line in logger.log:
                file.write(f"{line}\n")

    def rename(self,new_name,old_name):
        """
        Renames a file.
        
        Args:
            old_name (str): The current name of the file
            new_name (str): The new name of the file
        
        Returns:
            bool: Whether the file was renamed successfully
        """
        
        if os.path.isfile(new_name):
            self.log("Cannot overwrite pre-existing file")
        else:
            try:
                os.rename(old_name,new_name)
                return True
            except OSError as e:
                self.log(f"Cannot rename {old_name} to {new_name}: {e}")
        return False

    def write_json_receipt_to_file(self,filename,json_receipt):

        """
        Writes a JSON version of a receipt into a file
        
        Args:
            filename (str): Where the receipt should be saved
            json_receipt (str): Which receipt is to be saved
        """
        
        match = self.filename_search.search(filename)
        if match:
            new_name = match.group(1) + ".json"
        else:
            raise RuntimeError

        file_loc = os.path.join(self.processed_directory,new_name)
        
        try:
            with open(os.path.join(self.processed_directory,new_name),"w") as file:
                file.write(json.dumps(json_receipt,indent = 4))
        except OSError:
            self.log(f"Unable to write to file {file_loc}")
            raise OSError
            

    def accept(self,filename):
        """
        Puts a particular file into the Accepted folder to mark it as acceptable
        
        Args:
            filename (str): File to be accepted
        
        Returns:
            nothing
        """
        
        accepted_loc = os.path.join(self.accepted_directory,filename)
        receipt_loc = os.path.join(self.receipt_directory,filename)
        
        self.rename(accepted_loc,receipt_loc)

    def exclude(self,filename):
        """
        Puts a particular file into the Excluded folder to mark it as an issue
        
        Args:
            filename (str): File to be excluded
        
        Returns:
            nothing
            
        """    
        excluded_loc = os.path.join(self.excluded_directory,filename)
        receipt_loc = os.path.join(self.receipt_directory,filename)
        
        self.rename(excluded_loc,receipt_loc)

    def read_from_file(self,filename):
        """
        Reads a JSON file for a receipt that has already been processed.
        
        Args:
            filename (str): File to read from
            
        Returns:
            str: Textual representation of the JSON file
        
        """
        file_loc = os.path.join(self.processed_directory,filename)
    
        if os.path.isfile(file_loc):
            with open(os.path.join(self.processed_directory,filename),"r") as file:
                text = file.read()
                return text
        else:
            self.log("File does not exist")
            text = ""
            return text

    def get_directories(self):
        """Retrieve the directories that the file handler accesses."""
        
        self.processed_directory = config.processedReceiptsDirectory 
        self.receipt_directory = config.receiptsDirectory
        self.accepted_directory = config.acceptedReceiptsDirectory
        self.excluded_directory = config.excludedReceiptsDirectory
        self.log_directory = config.logDirectory
        
    def log(self, message: str) -> bool:
        if self.logger:
            self.logger.log_message(message)
            return True
        else:
            return False

if __name__ == '__main__':
    fh = FileHandler()
