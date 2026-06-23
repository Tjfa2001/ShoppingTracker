class DataExtractor:
    
    def __init__(self, connector):
        
        self.connector = connector
        
    def fetch(self,sql):
        
        try:
            data = self.connector.execute(sql)
        except:
            print("Error")
            data = -1
            
        return data   