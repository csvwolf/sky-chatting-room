#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket
import threading
from sockpack import *

s = socket.socket()

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
            receiver = receiveThread(c, addr)
            receiver.setDaemon(True)
            threadLock.acquire()
            lists.append(receiver)
            threadLock.release()
            receiver.start()
            print lists
            print 'Got connection from', addr
            # c.send('Thank you for connecting')

class receiveThread(threading.Thread):
    counter = 0

    def __init__(self, client, address):
        threading.Thread.__init__(self)
        self.client = client
        self.address = address

    def run(self):
        while True:
            try:
                msg = eval(recv_msg(self.client))
            except:
                break
            if msg:
                print msg
                if msg['type'] == 'message':
                    mutex.acquire()
                    if receiveThread.counter == 0:
                        threadLock.acquire()
                    receiveThread.counter += 1
                    mutex.release()
                    for receiver in lists:
                        if receiver.address != self.address:
                            print self.address, ' -> ', receiver.address
                            try:
                                send_msg(receiver.client, repr(msg).encode('utf8'))
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
                        break

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
    scanner.setDaemon(True)
    scanner.start()
    threadLock = threading.Lock()
    mutex = threading.Lock()

    for client in lists:
        client.client.close()


