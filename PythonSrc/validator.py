import master_dictionary as mast
import json

class Validator():

    master_dictionary = None

    def Validator(self):
        self.master_dictionary = mast.MasterDict()    

    def validate_receipt(self,receipt,json_receipt):
        totals_match = self.check_totals(receipt,json_receipt)
        if totals_match:
            pass
        else:
            return False
        
        item_lookup = self.lookup_items(receipt,json_receipt)

    def lookup_items(self,receipt,json_receipt):
        

    def check_totals(self,receipt_name,json_receipt):
        #for receipt in self.receipts:

            receipt = json.loads(json_receipt)
            total_for_receipt = float(receipt["total"])
            discount_for_receipt = receipt["discount"]
            item_sum_for_receipt = 0

            for item in receipt["items"]:

                if 'quantity' in item:
                    item_sum_for_receipt += float(item["price"])*float(item["quantity"])
                else:
                    item_sum_for_receipt += float(item["price"])

            if round(total_for_receipt,2) == round(item_sum_for_receipt,2):
                #self.fh.write_to_file(receipt_name,receipt)
                return True
            else:
                return False