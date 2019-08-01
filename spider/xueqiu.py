'''雪球数据组合追踪'''
import time
import logging

from utils.notice_email import send_email

logger=logging.getLogger('logger')

from SQL import get_conn
from SQL import Map
from spider.stock import Stock

from pprint import pprint

class XueQiu(Stock):
    host='https://xueqiu.com'
    def __init__(self):
        super().__init__()
        self.conn = get_conn()
        self.name="雪球"
    
    
    def collect(self,symbol):
        '''
        :param symbol:
        :param sid: 组合id
        :return:
        '''
        conn=get_conn()
        cur=conn.cursor()
        url=self.get_collect_url(symbol)
        resp=self.session.get(url)
        if resp.status_code!=200:
            logger.warning("数据请求失败")
            return None
        data=resp.json()
        new_adj = []
        rebalancing_histories=data['rebalancing']['rebalancing_histories']
        for item in rebalancing_histories:
            updated_at=item['updated_at']
            stock_symbol=item['stock_symbol']
            #通过调仓时间判断调仓是否有修改
            cur.execute(Map.CHECK_CHANGE,(stock_symbol,updated_at))
            count=cur.fetchone()[0]
            if count==0:
                new_adj.append(item)
                '''沒有调仓记录  添加'''
                '''create'''
        return new_adj
            
            
    def __str__(self):
        return self.name
    
   
    def start(self):
        logger.info("start %s"%self.name)
        start_time=time.time()
        #获取任务 执行任务 返回结果
        '''
        获取所有雪球的组合
        :return:
        '''
        cur=self.conn.cursor()
        cur.execute(Map.GET_STRATEGY,"雪球")
        data=cur.fetchall()
        for item in data:
            symbol=item[1]
            new_adj=self.collect(symbol)
            if new_adj:
                self.add_adj_records(item[0],new_adj)
                '''crate data'''
                strategy_url= self.symbol_generate_url(symbol)
                stock_names=[item['stock_name'] for item in new_adj]
                self.push(item[3],item[2],stock_names,strategy_url)
        end_time=time.time()
        logger.info("end %s" % self.name)
        return self.next_time(start_time,end_time)
        
    
    def next_time(self,start_time,end_time):
        '''计算下次轮训的时间间隔'''
        if end_time-end_time>self.INTERVAL_SECOND:
            return 0
        else:
            return round(self.INTERVAL_SECOND-(end_time-start_time),2)
       
            
    def add_adj_records(self,sid,data):
        '''
        添加调仓记录
        :param sid: 组合id
        :param data:  调仓信息
        :return:
        '''
        cur=self.conn.cursor()
        items=[]
        for item in data:
            items.append((
                sid,
                item['stock_symbol'],
                item['stock_name'],
                item['prev_weight'],
                item['weight'],
                item['price'],
                item['updated_at'])
            )
        cur.executemany(Map.CREATE_POSITION_ADJST,items)
        # cur.execute(Map.CREATE_POSITION_ADJST,items[0])
        self.conn.commit()
        logger.info('create adjust records:%s-%s '%(sid,data))
    def get_collect_url(self,symbol):
        url="%s/cubes/rebalancing/show_origin.json?rb_id=58099743&cube_symbol=%s"%(self.host,symbol)
        return url


    def load_session(self):
        headers={
            "Host": "xueqiu.com"
        }
        self.session.headers=headers
    
    @staticmethod
    def url_parser_symbol(url):
        '''
        :param url:https://xueqiu.com/p/ZH1890323
        :return:
        '''
        symbol=url.split('/')[-1]
        return symbol
    
    @staticmethod
    def symbol_generate_url(symbol):
        url="https://xueqiu.com/p/%s"%symbol
        return url
    
    def push(self,email,strategy_name,names,strategy_url):
        '''
        :param email: 收件人
        :param strategy_name: 组合名称
        :param names:  调仓股票
        :param strategy_url:组合链接
        :return:
        '''
        if len(names)<3:
            names=",".join(names)
        else:
            names=",".join(names[:3])+"等"
        text = '''<h3><a href="{href}">您订阅的组合({s_name}) {names}有调仓更新</a></h3>'''.format(href=strategy_url,s_name=strategy_name,names=names)
        try:
            send_email('%s'%email,text)
            logger.info("email send OK:%s"%email)
        except Exception as e:
            logger.error("email send error %s:%s"%(email,e))

    
xueqiu=XueQiu()

if __name__=="__main__":
    xueqiu.start()

'''
{'created_at': 1564382243709,
                                            'id': 231342813,
                                            'net_value': 0.2343,
                                            'prev_net_value': 0.11606615,
                                            'prev_price': 38.63,
                                            'prev_target_volume': 0.00300339,
                                            'prev_target_weight': 7.92,
                                            'prev_volume': 0.00300456,
                                            'prev_weight': 7.92  调仓前仓位,
                                            'prev_weight_adjusted': 7.9 ,
                                            'price': 38.51,
                                            'proactive': True,
                                            'rebalancing_id': 58099743,
                                            'stock_id': 1000882,
                                            'stock_name': '中国太保'  股票名称,
                                            'stock_symbol': 'SH601601'  股票代码,
                                            'target_volume': 0.00608304 ,
                                            'target_weight': 16.0,
                                            'updated_at': 1564382243709  调仓时间,
                                            'volume': 0.00608304,
                                            'weight': 16.0  调仓后仓位}


'''
''''添加分享后 加入分享链接 和用户id'''