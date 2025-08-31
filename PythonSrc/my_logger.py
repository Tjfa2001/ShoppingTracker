import datetime

if __name__ == '__main__':
    current_time = datetime.datetime.now()
    print(current_time.strftime("%A %d %B %Y, %H:%M -> "))
    print("HELLO")

class Logger:

    log = None
    file_handler = None

    def __init__(self,file_handler):
        self.log = []
        self.file_handler = file_handler

    def log_message(self,message):
        current_time = self.get_time()
        timed_message = current_time + message
        self.log.append(timed_message)

    def write_to_file(self):
        self.file_handler.write_logger_to_file(self)

    def get_time(self):
        current_time = datetime.datetime.now().strftime("%A %d %B %Y, %H:%M -> ")
        return current_time