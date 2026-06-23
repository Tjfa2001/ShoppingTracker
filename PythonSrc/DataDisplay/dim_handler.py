class DimHandler():
    
    def __init__():
        pass
    
    @staticmethod
    def get_dims(dim_object:str) -> tuple[int, int]:
        dims = tuple(dim_object.split(sep='x'))
        height = int(dims[0])
        width = int(dims[1]) 
        return (height,width)
        
if __name__ == '__main__':
    to_try = "300x400"
    print(DimHandler.get_dims(to_try))