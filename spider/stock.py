'''基类  接口  '''
import requests

session=requests.session()


class Stock:
    host=''
    #查询时间间隔
    INTERVAL_SECOND=15
    def __init__(self):
        '''初始化'''
        self.session=session
        self.load_session()
    
    def init(self):
        '''初始化'''
        pass
    
    
    def collect(self,*args):
        '''实现数据采集'''
        pass
    def load_session(self):
        pass
    
    
    def __str__(self):
        return "股票"