

class Field():
    def __init__(self, xpath: str, error_xpath: str, ) -> None:
        self.xpath = xpath
        self.error_xpath = error_xpath
        
    def get_xpath(self, ):
        return self.xpath
    
    def get_error_xpath(self, ):
        return self.error_xpath
    
    def set_value(self, *values):
        raise NotImplementedError("É precis implementar a inserção do campo")