import master_dictionary as mast
import name_selector as ns
import json

class Validator():

    master_dictionary = None
    mast_dict_obj = None

    def __init__(self):
        self.mast_dict_obj = mast.MasterDict()
        self.master_dictionary = json.loads(self.mast_dict_obj.master)

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
                #print(f"{item_name} in Dictionary")
                new_name = self.master_dictionary[item_name]
                
            else:
                print(f"{item_name} not in Dictionary")
                name_selector = ns.NameSelector(item_name) 
                new_name = name_selector.new_name
                print(f"Got {new_name}")
                self.master_dictionary.update({item_name:new_name})

            if new_name is None:
                print("Not changing name")
            elif item_name != self.master_dictionary[item_name]:
                print(f"Changing {item_name} to {self.master_dictionary[item_name]}")    
                receipt_items[i]["name"] = self.master_dictionary[item_name]

        self.mast_dict_obj.write_to_file(self.master_dictionary)
        dictionary["items"] = receipt_items
        
        return dictionary

    def check_totals(self,json_receipt):

            receipt = json.loads(json_receipt)
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
                return False