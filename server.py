#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket
import threading
import time
from sockpack import *
import json
from aes import *

"""
收发基于读者写者模型, 采用对称加密
"""

s = socket.socket()

#host = '115.28.26.5'
host = socket.gethostname() # 获取本地ip
port = 1234
s.bind((host, port))

lists = []      # 连接数组
s.listen(5)     # 队列长度最大为5

class scanThread(threading.Thread):

    """
    持续监测是否有新客户端连入
    """

    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        while True:
            c, addr = s.accept()        # 阻塞等待连入
            receiver = receiveThread(c, addr, 'receiver')
            receiver.setDaemon(True)    # 关闭主进程时随之关闭
            threadLock.acquire()
            lists.append(receiver)
            threadLock.release()
            receiver.start()
            #print lists
            #print 'Got connection from', addr
            # c.send('Thank you for connecting')

class protectionThread(threading.Thread):

    """
    保持长连接增设的线程
    """

    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        c = socket.socket()
        c.connect((host, port))

        while 1:
            send_msg(c, encrypt(json.dumps({'type': 'command', 'content': 'keeper'}), getPassword()))
            time.sleep(60)


class receiveThread(threading.Thread):
    """
    接收消息的线程
    简单划分为每个线程一个
    """

    counter = 0     # 读者写者模型中的计数君

    def __init__(self, client, address, type):
        threading.Thread.__init__(self)
        self.client = client
        self.address = address
        self.type = type

    def run(self):
        while True:
            try:
                msg = json.loads(decrypt(recv_msg(self.client), getPassword()))
            except:
                break
            if msg:
                #print msg
                if msg['type'] == 'message':
                    # 以下是读者的操作
                    mutex.acquire()
                    if receiveThread.counter == 0:
                        threadLock.acquire()
                    receiveThread.counter += 1
                    mutex.release()
                    for receiver in lists:
                        if receiver.address != self.address and receiver.type != 'protector':
                            #print self.address, ' -> ', receiver.address
                            try:    # 如果出错,则表示这个链接由于某些原因已经断开
                                send_msg(receiver.client, encrypt(json.dumps(msg), getPassword()))
                            except Exception, e:
                                lists.remove(receiver)
                    mutex.acquire()
                    receiveThread.counter -= 1
                    if receiveThread.counter == 0:
                        threadLock.release()
                    mutex.release()
                    # 以上是读者的操作
                elif msg['type'] == 'command':
                    if msg['content'] == 'quit':
                        threadLock.acquire()
                        lists.remove(self)
                        threadLock.release()
                        self.client.close()
                        break
                    elif msg['content'] == 'keeper':    # 如果是保持长连接的线程发送过来的持续化消息
                        self.type = 'protector'
                        recv_msg(self.client)
                        send_msg(self.client, encrypt(json.dumps({'type': 'command', 'content': 'keep'}), getPassword()))

# while True:
#     c, addr = s.accept()
#     lists.append({'client': c, 'address': addr})
#     print lists
#     print 'Got connection from', addr
#     c.send('Thank you for connecting')
#     for client in lists:
#         msg = client['client'].recv(1024)
#         if msg:
#             print msg
#             for receiver in lists:
#                 if receiver != client:
#                     receiver['client'].sendall(msg)
#     #word = raw_input('>')
#     #for c in lists:
#         #c['client'].sendall(word)

if __name__ == '__main__':
    scanner = scanThread()
    scanner.start()
    protectionThread().start()
    threadLock = threading.Lock()
    mutex = threading.Lock()

    # for client in lists:
    #     client.client.close()


