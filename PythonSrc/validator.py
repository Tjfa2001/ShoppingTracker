import ShoppingTracker.PythonSrc.master_dictionary as mast
import ShoppingTracker.PythonSrc.name_selector as ns
import json

class Validator():

    master_dictionary = None
    mast_dict_obj = None
    logger = None

    def __init__(self, logger):
        self.mast_dict_obj = mast.MasterDict()
        self.master_dictionary = json.loads(self.mast_dict_obj.master)
        self.logger = logger

    def validate_receipt(self,json_receipt):
        
        totals_match = self.check_totals(json_receipt)
        if totals_match:
            pass
        else:
            return False
        
        item_lookup = self.lookup_items(json_receipt)
        
        return item_lookup

    def lookup_items(self,json_receipt):

        # Gets the items from the json receipt
        dictionary = json.loads(json_receipt)
        receipt_items = dictionary["items"]

        for i,item in enumerate(receipt_items):

            item_name = item["name"]

            if item_name in self.master_dictionary:
                new_name = self.master_dictionary[item_name]
                
            else:
                self.log_message(f"{item_name} not in Dictionary")
                name_selector = ns.NameSelector(item_name) 
                new_name = name_selector.new_name
                self.log_message(f"Got {new_name} from user")
                self.master_dictionary.update({item_name:new_name})

            if new_name is None:
                self.log_message("Not changing name")
            elif item_name != self.master_dictionary[item_name]:
                self.log_message(f"Changing {item_name} to {self.master_dictionary[item_name]}")    
                receipt_items[i]["name"] = self.master_dictionary[item_name]

        self.mast_dict_obj.write_to_file(self.master_dictionary)
        dictionary["items"] = receipt_items
        
        return dictionary

    def check_totals(self,json_receipt):

            receipt = json.loads(json_receipt)
            
            if 'total' not in receipt:
                return False
            else:
                total_for_receipt = float(receipt["total"])
                
            item_sum_for_receipt = 0

            for item in receipt["items"]:

                if 'quantity' in item:
                    item_sum_for_receipt += float(item["price"])*float(item["quantity"])
                else:
                    item_sum_for_receipt += float(item["price"])

            if round(total_for_receipt,2) == round(item_sum_for_receipt,2):
                return True
            else:
                self.log_message(f"Total {total_for_receipt} does not match sum of items {item_sum_for_receipt}") 
                return False
            
    def log_message(self,message):
        self.logger.log_message(message)