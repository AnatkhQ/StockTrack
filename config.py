import os
# 数据库公开使用
DATABASE_CONFIG={
        "host":'47.107.75.121',
        "port":3306,
        "user": 'stock',
        "password": '123456',
        "database":"stock"
    }

EMAIL_CONFIG={
    "host":"smtp.qq.com",
    "encoding":"utf-8",
    'username':os.environ.get('email'),
    'password':os.environ.get('epwd'),
    'from':os.environ.get('email'),
}


DEBUG=False