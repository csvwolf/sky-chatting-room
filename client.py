#!/usr/bin/env python
# -*- coding:utf-8 -*-

import socket
import threading

"""
一个过时的Terminal端,如果需要使用,请按照gui.py补全
"""

s = socket.socket()

host = socket.gethostname()
port = 1234
status = True
s.connect((host, port))

class inputThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        while 1:
            if (status):
                word = raw_input('>')
                s.sendall(word)

class receiveThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        while 1:
            print s.recv(1024)

if __name__ == '__main__':
    input = inputThread()
    receiver = receiveThread()

    input.start()
    receiver.start()

    print 'Client Start'

# print s.recv(1024)
# s.sendall('Hello World')
# while 1:
#     word = raw_input('>')
#     s.sendall(word)
#     print s.recv(1024)
