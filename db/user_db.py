#--coding:utf-8--
# @Time    : 2020/12/27/027 22:41
# @Author  : panyuangao
# @File    : user_db.py
# @PROJECT : chatRoom
from db import handle_mysql

def checkUser(account): # 通过account查询用户信息
    mysql = handle_mysql.MySQL()
    sql_select_account = "SELECT account,password,nickname FROM user WHERE account = '%s'" %account
    userInfo = mysql.select(sql_select_account)
    mysql.conn_close()
    return userInfo

def insertUser(account, password, nickname): # 插入用户信息
    mysql = handle_mysql.MySQL()
    sql_insert = "INSERT INTO user(account,password,nickname) VALUES('%s','%s','%s')" % (account, password, nickname)
    mysql.insert(sql_insert)
    mysql.conn_close()




