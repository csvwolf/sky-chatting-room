#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket

s = socket.socket()

host = socket.gethostname()
port = 1234
s.bind((host, port))

lists = []
s.listen(5)

while True:
    c, addr = s.accept()
    lists.append({'client': c, 'address': addr})
    print lists
    print 'Got connection from', addr
    c.send('Thank you for connecting')
    for client in lists:
        msg = client['client'].recv(1024)
        if msg:
            print msg
            for receiver in lists:
                if receiver != client:
                    receiver['client'].sendall(msg)
    #word = raw_input('>')
    #for c in lists:
        #c['client'].sendall(word)

for client in lists:
    client['client'].close()


