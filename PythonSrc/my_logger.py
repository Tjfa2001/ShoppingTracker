if __name__ == '__main__':
    print("HELLO")

class Logger:

    def __init__(self):
        self.log = []

    def log_message(self,message):
        self.log.append(message)