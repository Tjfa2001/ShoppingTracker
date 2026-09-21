"""
Module to log state and errors from Receipt Reader Application
"""
import datetime

if __name__ == '__main__':
    print("This module is not meant to be run directly")

class Logger:

    """Logger class for logging messages with timestamps"""
    log = None
    file_handler = None
    debug = False

    # Initialize the Logger with a FileHandler instance
    def __init__(self,file_handler,**kwargs):
        self.log = []
        self.file_handler = file_handler
        if 'debug' in kwargs:
            self.debug = kwargs['debug']

    def log_message(self,message: str):
        """Log a message with a timestamp"""
        current_time = self.get_time()
        timed_message = current_time + message
        self.log.append(timed_message)
        if self.debug:
            print(timed_message)

    def log_error(self,error_message: str):
        """Log an error with a timestamp"""
        current_time = self.get_time()
        timed_error = current_time + error_message
        self.log.append(timed_error)
        if self.debug:
            print(timed_error)

    def log_list_log(self, list_log: list[str]):
        """Log another log in list format"""
        if isinstance(list_log,list):
            for item in list_log:
                self.log_message(item)
        else:
            self.log_error(f"Tried to log {list_log} but {list_log} is not a list")

    def write_to_file(self):
        """Write the log messages to a file using the FileHandler"""
        self.file_handler.write_logger_to_file(self)

    def get_time(self, time_format="%A %d %B %Y, %H:%M -> "):
        """Get the current time formatted as a string"""
        current_time = datetime.datetime.now().strftime(time_format)
        return current_time

if __name__ == '__main__':
    print("This module is not meant to be run directly")
