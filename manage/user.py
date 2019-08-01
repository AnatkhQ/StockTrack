from pymysql.err import InterfaceError
from SQL import get_conn


def crate_user(email):
    '''添加用户'''
    conn=get_conn()
    cur=conn.cursor()
    try:
        cur.execute('''insert into user(email) VALUES('%s')'''%email)
        conn.commit()
    except InterfaceError:
        raise TypeError("员工已存在")
    