#--coding:utf-8--
# @Time    : 2020/12/15/015 0:07
# @Author  : panyuangao
# @File    : client.py
# @PROJECT : chatRoom
import tkinter
from tkinter import messagebox
import json,time
import threading
import select
from socket import *
from client import client_draw

class ChatRoom(object):
    def connect(self): #配置连接
        self.s = socket(AF_INET, SOCK_STREAM)
        remote_host = gethostname() #获取计算机名称
        port = 1200  #设置端口号
        self.s.connect((remote_host, port))  # 发起连接
        print("从%s成功连接到%s" %(self.s.getsockname(),self.s.getpeername()))
        return self.s

    def recive(self,s): # 监听消息
        self.my = [s]
        while True:
         rs, ws, es = select.select(self.my, [], [])
         if s in rs:
             try:
                 data = s.recv(1024).decode('utf-8')
                 data_dict = json.loads(data)
                 type = data_dict["type"] # 根据服务端返回的type值，进入不同逻辑
                 if type == "login": # 登录逻辑
                     if "000000" == data_dict["code"]: #code返回000000，跳转聊天页面
                         nickname = data_dict["nickname"]
                         self.chat_interface(nickname)
                     else:
                         tkinter.messagebox.showinfo(title='登录提示', message=data_dict["msg"])
                 elif type == "register": # 注册逻辑
                     if "000000" == data_dict["code"]:  #code返回000000，跳转聊天页面
                         nickname = data_dict["nickname"]
                         tkinter.messagebox.showinfo(title='进入聊天室', message=data_dict["msg"])
                         self.chat_interface(nickname)
                     else:
                         tkinter.messagebox.showinfo(title='注册提示', message=data_dict["msg"])
                 elif type == "chat": # 聊天逻辑
                     message = data_dict["message"]
                     nickname = data_dict["nickname"]
                     isMy = data_dict["isMy"]
                     times = " "+ nickname + "\t" + time.strftime("%H:%M:%S",time.localtime())+ '\n'
                     self.txtMsgList.insert(tkinter.END, times,"DimGray") # 聊天页面，发送人以及发送时间展示
                     if "yes" == isMy: # 如果是自己发的消息，字体使用'DarkTurquoise'，如果是别人发的消息，字体使用'Black'
                        self.txtMsgList.insert(tkinter.END,  " "+ message + "\n\n",'DarkTurquoise')
                     else:
                         self.txtMsgList.insert(tkinter.END, " " + message + "\n\n", 'Black')
                     self.txtMsgList.see(tkinter.END) # 插入消息时，自动滚动到底部

             except Exception as e:
                 print(e)
                 exit()


    def register_interface(self): # 进入注册界面
        client_draw.draw_register(self)

    def chat_interface(self,nickname): #进入聊天页面
        client_draw.draw_chat(self,nickname)

    def return_login_interface(self): #返回登录页面
        self.label_nickname.destroy() #将不需要的label_nickname控件先销毁
        self.input_nickname.destroy() #将不需要的input_nickname控件先销毁
        self.label_password.destroy() #将不需要的label_password控件先销毁
        self.input_password.destroy() #将不需要的input_password控件先销毁
        client_draw.draw_login(self)


    def verify_register(self): # 获取输入框内容，进行注册验证
        account = self.input_account.get()
        password = self.input_password.get()
        nickname = self.input_nickname.get()
        try:
            register_data = {}
            register_data["type"] = "register"
            register_data["account"] = account
            register_data["password"] = password
            register_data["nickname"] = nickname
            data = json.dumps(register_data) #将register_data由dict格式转为json字符串，便于网络传输
            self.s.send(data.encode('utf-8'))
        except Exception as e:
            print(e)

    def verify_login(self): # 获取输入框内容，进行登录信息验证
        account = self.input_account.get()
        password = self.input_password.get()
        try:
          login_data = {}
          login_data["type"] = "login"
          login_data["account"] = account
          login_data["password"] = password
          data = json.dumps(login_data) #将login_data由dict格式转为json字符串，便于网络传输
          self.s.send(data.encode('utf-8'))
        except Exception as e:
          print(e)


    def sendMsg(self):#获取输入框内容，发送消息
        message = self.txtMsg.get('0.0', tkinter.END).strip()
        if not message:
            tkinter.messagebox.showinfo(title='发送提示', message="发送内容不能为空，请重新输入")
            return
        self.txtMsg.delete('0.0', tkinter.END)
        try:
          chat_data = {}
          chat_data["type"] = "chat"
          chat_data["message"] = message
          data = json.dumps(chat_data) #将chat_data由dict格式转为json字符串，便于网络传输
          self.s.send(data.encode('utf-8'))
        except Exception as e:
          print(e)

    def sendMsgEvent(self,event):#发送消息事件
        if event.keysym =='Return': #如果捕捉到键盘的回车按键，触发消息发送
            self.sendMsg()

    def on_closing(self):  # 聊天页面，点击右上角退出时执行
        if messagebox.askokcancel("退出提示", "是否离开聊天室？"):
            self.root.destroy()

def main():
    chatRoom = ChatRoom()
    client = chatRoom.connect()
    t = threading.Thread(target=chatRoom.recive, args=(client,)) # 创建一个线程，监听消息
    t.start()
    chatRoom.root = tkinter.Tk()  # 创建主窗口,用于容纳其它组件
    client_draw.draw_login(chatRoom) # 登录界面控件创建、布局
    tkinter.mainloop() # 进入事件（消息）循环


if __name__ == '__main__':
    main()

