import os


class MasterDict:

    dictionary_location = None
    master = None

    def __init__(self):
        self.get_directory()
        self.read_from_file()

    def get_directory(self):
        self.dictionary_location = os.path.join(os.path.abspath("."),r"ShoppingTracker\MasterDictionary\MastDict.json")

    def add_to_master():
        pass

    def remove_from_master():
        pass

    def write_to_file(self):
        pass

    def read_from_file(self):
        file_exists = os.path.isfile(self.dictionary_location)

        if file_exists:
            print("Reading")
            with open(self.dictionary_location,"r") as file:
                self.master = file.read()
        else:
            print("No dictionary to read :(")
    
m = MasterDict()