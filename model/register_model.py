#--coding:utf-8--
# @Time    : 2020/12/28/028 23:10
# @Author  : panyuangao
# @File    : register_model.py
# @PROJECT : chatRoom
from db import user_db
import json

def register(self, data_dict):  # 注册逻辑
    account = data_dict["account"].strip()
    password = data_dict["password"].strip()
    nickname = data_dict["nickname"].strip()
    data = {}
    if account and password and nickname: #account、password、nickname均不为空，才走注册验证逻辑
        code, msg = register_check(account, password, nickname)
    elif not account:
        code = "600002"
        msg = "注册账号不能为空"
    elif not password:
        code = "600003"
        msg = "注册密码不能为空"
    elif not nickname:
        code = "600004"
        msg = "注册昵称不能为空"

    if code == "000000":
        self.users[self] = nickname
        data["nickname"] = nickname

    data["type"] = "register"
    data["code"] = code
    data["msg"] = msg
    data = json.dumps(data)
    self.sendLine(data.encode("utf-8"))


def register_check(account,password,nickname): #注册验证逻辑
    checkUser = user_db.checkUser(account) #通过账号查询用户信息
    if len(checkUser) > 0: #如果查询到用户信息，表示该账号已经注册
        data = ("600005","账号【%s】已注册" %account)
    else:
        user_db.insertUser(account,password,nickname) #将用户信息插入数据库
        data = ("000000","账号【%s】注册成功,点击“确定”进入聊天页面" %account)
    return data