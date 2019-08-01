import pymysql
import config



def get_conn():
    return pymysql.connect(**config.DATABASE_CONFIG)
