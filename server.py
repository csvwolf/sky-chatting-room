#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket
import threading
import time
from sockpack import *
import json
from aes import *

s = socket.socket()

#host = '115.28.26.5'
host = socket.gethostname()
port = 1234
s.bind((host, port))

lists = []
s.listen(5)

class scanThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        while True:
            c, addr = s.accept()
            receiver = receiveThread(c, addr, 'receiver')
            receiver.setDaemon(True)
            threadLock.acquire()
            lists.append(receiver)
            threadLock.release()
            receiver.start()
            #print lists
            #print 'Got connection from', addr
            # c.send('Thank you for connecting')

class protectionThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        c = socket.socket()
        c.connect((host, port))

        while 1:
            send_msg(c, encrypt(json.dumps({'type': 'command', 'content': 'keeper'}), getPassword()))
            time.sleep(60)


class receiveThread(threading.Thread):
    counter = 0

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
                    mutex.acquire()
                    if receiveThread.counter == 0:
                        threadLock.acquire()
                    receiveThread.counter += 1
                    mutex.release()
                    for receiver in lists:
                        if receiver.address != self.address and receiver.type != 'protector':
                            #print self.address, ' -> ', receiver.address
                            try:
                                send_msg(receiver.client, encrypt(json.dumps(msg), getPassword()))
                            except Exception, e:
                                lists.remove(receiver)
                    mutex.acquire()
                    receiveThread.counter -= 1
                    if receiveThread.counter == 0:
                        threadLock.release()
                    mutex.release()
                elif msg['type'] == 'command':
                    if msg['content'] == 'quit':
                        threadLock.acquire()
                        lists.remove(self)
                        threadLock.release()
                        self.client.close()
                        break
                    elif msg['content'] == 'keeper':
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


