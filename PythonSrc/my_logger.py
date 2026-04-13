import datetime

if __name__ == '__main__':
    print("This module is not meant to be run directly")

class Logger:

    # Logger class for logging messages with timestamps
    log = None
    file_handler = None
    debug = False

    # Initialize the Logger with a FileHandler instance
    def __init__(self,file_handler,**kwargs):
        self.log = []
        self.file_handler = file_handler
        if 'debug' in kwargs:
            self.debug = kwargs['debug']

    # Log a message with a timestamp
    def log_message(self,message):
        current_time = self.get_time()
        timed_message = current_time + message
        self.log.append(timed_message)
        if self.debug:
            print(timed_message)
            
    # Log an error with a timestamp
    def log_error(self,error_message):
        current_time = self.get_time()
        timed_error = current_time + error_message
        self.log.append(timed_error)
        if self.debug:
            print(timed_error)
            
    # Log another log in list format
    def log_list_log(self,list_log):
        if type(list_log) is list:
            [self.log_message(x) for x in list_log]
        else:
            self.log_error(f"Tried to log {list_log} but {list_log} is not a list")
    
    # Write the log messages to a file using the FileHandler
    def write_to_file(self):
        self.file_handler.write_logger_to_file(self)

    # Get the current time formatted as a string
    def get_time(self):
        current_time = datetime.datetime.now().strftime("%A %d %B %Y, %H:%M -> ")
        return current_time