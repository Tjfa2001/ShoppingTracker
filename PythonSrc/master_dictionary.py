import os
import json
import config

class MasterDict:

    dictionary_location = None
    master = None
    mast_dict_json = None

    def __init__(self):
        self.get_directories()
        self._read_from_file()
        self.load_file_to_json()

    def load_file_to_json(self):
        self.mast_dict_json = json.loads(self.master)

    def get_directories(self):
        self.dictionary_location = config.MAST_DICT_LOC

    def update(self,item_name,new_name):
        self.mast_dict_json.update({item_name:new_name})

    def remove_from_master(self,item_name):
        self.mast_dict_json.pop(item_name)

    def write_to_file(self):
        with open(self.dictionary_location,"w",encoding="utf-8") as file:
            file.write(json.dumps(self.mast_dict_json,indent=4))

    def _read_from_file(self):

        """Reads the master dictionary in from the saved file"""
        file_exists = os.path.isfile(self.dictionary_location)

        if file_exists:
            with open(self.dictionary_location,"r",encoding="utf-8") as file:
                self.master = file.read()
        else:
            # If the master dictionary file doesn't exist, initialize an empty dictionary
            # and create the file so downstream code (like Validator) can json.loads() it.
            empty = {}
            self.master = json.dumps(empty)
            try:
                os.makedirs(os.path.dirname(self.dictionary_location), exist_ok=True)
                with open(self.dictionary_location, "w",encoding="utf-8") as file:
                    file.write(self.master)
            except Exception:
                # If we can't write the file for some reason, keep master as an empty JSON string
                pass

m = MasterDict()