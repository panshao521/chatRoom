#--coding:utf-8--
# @Time    : 2020/12/27/027 22:25
# @Author  : panyuangao
# @File    : handle_mysql.py
# @PROJECT : chatRoom

import pymysql

class MySQL():
    def __init__(self):
        # 第一步：打开数据库连接
        self.conn = pymysql.connect(
            host = "39.100.106.61",
            port = 3306,
            user = "root",
            passwd = "123456",
            db = "aa",
            charset = "utf8")
        self.conn.select_db("chat")

    def insert(self,SQL):
        cursor = self.conn.cursor() #第二步，获取游标
        try:#第三步：执行SQL
            cursor.execute(SQL)
            cursor.close()  #第四步：关闭游标
            self.conn.commit()   #第五步：提交事务
            # print("数据入库成功")
        except pymysql.Error as e:
            print("Mysql Error %d: %s" % (e.args[0], e.args[1]))

    def select(self,SQL):
        cursor = self.conn.cursor() #第二步，获取游标
        try:#第三步：执行SQL
            cursor.execute(SQL)  # 读取所有user表中的数据，默认存cursor中
            resSet = cursor.fetchall()  # 获取表中的全部数据
            cursor.close()  #第四步：关闭游标
            self.conn.commit()   #第五步：提交事务
            return resSet
        except pymysql.Error as e:
            print("Mysql Error %d: %s" % (e.args[0], e.args[1]))

    def conn_close(self):
        self.conn.close()  # 第六步：关闭连接


if __name__ == '__main__':
    mysql = MySQL()
    sql = "SELECT nickname FROM user "
    resSet = mysql.select(sql)
    print(resSet[0][0])
