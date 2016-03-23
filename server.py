#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket
import threading

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
            lists.append({'client': c, 'address': addr})
            receiveThread(c, addr).start()
            print lists
            print 'Got connection from', addr
            c.send('Thank you for connecting')

class receiveThread(threading.Thread):
    def __init__(self, client, address):
        threading.Thread.__init__(self)
        self.client = client
        self.address = address

    def run(self):
        while True:
            try:
                msg = self.client.recv(1024)
            except:
                break
            if msg:
                print msg
                for receiver in lists:
                    if receiver['address'] != self.address:
                        print self.address, ' -> ', receiver['address']
                        try:
                            receiver['client'].sendall(msg)
                        except Exception, e:
                            print '已登出该用户'
                            lists.remove(receiver)
                            print lists

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

# for client in lists:
#     client['client'].close()


