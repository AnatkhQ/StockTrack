from SQL import get_conn
from SQL import Map
class SqlStack:
    
    @staticmethod
    def creaet_strategy(*args):
        ''':arg
            name,web,user_id
        '''
        con=get_conn()
        cur=con.cursor()
        # args=(name,web,user_id)
        try:
            cur.execute(Map.CREATE_STRATEGY, args)
            con.commit()
            return True
        except:
            return False