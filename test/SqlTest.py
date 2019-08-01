
from SQL import SqlSpider
from SQL.SqlSpider import SqlStack

class sqlTest():
    
    @staticmethod
    def create_strategy():
        SqlStack.creaet_strategy('测试',"雪花",1)
        
    
    
sqlTest.create_strategy()