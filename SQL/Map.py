
#创建组合
CREATE_STRATEGY='''
insert into strategy(name,web,create_time,update_time,user_id) VALUES (%s,%s,now(),now(),%s);
'''


#获取组合信息

GET_STRATEGY='''
select strategy.id,strategy.symbol,name,email from strategy,user where strategy.user_id=user.id and  web=%s

'''

CHECK_CHANGE='''select count(1) from position_adjst where stock_symbol=%s and updated_at=%s'''


#添加调仓记录
CREATE_POSITION_ADJST='''
insert into position_adjst(strategy_id,stock_symbol,stock_name,prev_weight,weight,price,updated_at) values(%s,%s,%s,%s,%s,%s,%s)
'''
