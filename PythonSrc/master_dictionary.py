import os
import json
import config

class MasterDict:

    dictionary_location = None
    master = None
    mast_dict_json = None

    def __init__(self):
        self.get_directories()
        self.read_from_file()
        self.mast_dict_json = json.loads(self.master)

    def get_directories(self):
        self.dictionary_location = config.masterDictionaryLocation

    def update(self,item_name,new_name):
        self.mast_dict_json.update({item_name:new_name})

    def remove_from_master(self,item_name):
        self.mast_dict_json.pop(item_name)

    """
    From before I refactored writing of the master dictionary from the master dictionary class and not the validator
    
    def write_to_file(self,new_master):
        self.master = new_master
        with open(self.dictionary_location,"w") as file:
            file.write(json.dumps(new_master,indent=4))"""

    def write_to_file(self):
        with open(self.dictionary_location,"w") as file:
            file.write(json.dumps(self.mast_dict_json,indent=4))

    def read_from_file(self):
        file_exists = os.path.isfile(self.dictionary_location)

        if file_exists:
            with open(self.dictionary_location,"r") as file:
                self.master = file.read()
        else:
            # If the master dictionary file doesn't exist, initialize an empty dictionary
            # and create the file so downstream code (like Validator) can json.loads() it.
            empty = {}
            self.master = json.dumps(empty)
            try:
                os.makedirs(os.path.dirname(self.dictionary_location), exist_ok=True)
                with open(self.dictionary_location, "w") as file:
                    file.write(self.master)
            except Exception:
                # If we can't write the file for some reason, keep master as an empty JSON string
                pass
    
m = MasterDict()