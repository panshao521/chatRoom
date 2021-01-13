#--coding:utf-8--
# @Time    : 2020/12/28/028 23:07
# @Author  : panyuangao
# @File    : login_model.py
# @PROJECT : chatRoom
from db import user_db
import json

def login(self,data_dict):#登录逻辑
    account = data_dict["account"].strip()
    password = data_dict["password"].strip()
    data = {}
    if account and password: #账号密码均不为空，才进入登录验证逻辑
        code,msg,nickname = login_check(account, password)
    elif not account:
        code = "700001"
        msg = "登录账号不能为空"
    elif not password:
        code = "700002"
        msg = "登录密码不能为空"

    if code == "000000": # code为000000时，表示登录成功，将连接对象以及昵称，加到users里，便于后续遍历发送消息
        self.users[self] = nickname
        data["nickname"] = nickname
    data["type"] = "login"
    data["code"] = code
    data["msg"] = msg
    data = json.dumps(data)
    self.sendLine(data.encode("utf-8"))

def login_check(account, password): #登录校验
    userInfo = user_db.checkUser(account) #通过账号查询数据库，获取账号、密码、昵称
    if len(userInfo) == 0: #未查询出数据，表示该账号未注册
        data = ("700003", "账号【%s】未注册，请注册后再登录！" % account, None)
    elif password != userInfo[0][1]: #查询出的密码与接收到的不致，表示密码不正确
        data = ("700004", "密码错误，请重新输入", None)
    else:
        nickname = userInfo[0][2] #登录成功，获取昵称
        data = ("000000", "账号【%s】登录成功" % account, nickname)
    return data