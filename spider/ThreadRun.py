'''多线程数据抓取'''
import threading
import time
import logging
logger=logging.getLogger('logger')
from spider import Support_class


class StockThread(threading.Thread):
    def __init__(self,stock):
        self.stock=stock
        super().__init__()
    
    def run(self):
        while True:
            sleep_time=self.stock.start()
            logger.info("waiting:%s"%sleep_time)
            time.sleep(sleep_time)
        
    def stop(self):
        self.stopped = True
        
def main():
    threads=[]
    for stock in Support_class:
        thread=StockThread(stock)
        thread.start()
        logger.info("%s start %s"%(thread.name,stock))
        threads.append(thread)
    