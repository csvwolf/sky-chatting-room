#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Tkinter import *
import tkMessageBox
import socket
import threading
from sockpack import *

root = Tk()
root.title('chatting-room')
text = Text(root)
text.insert(INSERT, "Hello.....")
text.grid(row = 0, columnspan=15)
text.tag_config('self', foreground='red')
text['state'] = DISABLED

#scroller = Scrollbar(text, orient=VERTICAL)

s = socket.socket()

host = '115.28.26.5'
port = 1234
status = True
try:
    s.connect((host, port))
except Exception, e:
    tkMessageBox.showerror("连接失败", "服务器暂未开放")
    exit()

class receiveThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.counter = 0

    def run(self):
        while 1:
            try:
                word = recv_msg(s)
            except Exception, e:
                break
            if word:
                word = eval(word)
                text['state'] = NORMAL
                text.insert(END, '\n' + word['author'] + ': ' + word['content'])
                self.counter += 1
                text.yview_scroll(self.counter, 'unit')
                text['state'] = DISABLED

def postMessage():
    length = len(messageInput.get())
    if length > 0:
        text['state'] = NORMAL
        content = userInput.get() + ': ' + messageInput.get()
        text.insert(END, '\n' + content, 'self')
        receiver.counter += 1
        text.yview_scroll(receiver.counter, 'unit')
        content = "{'type': 'message', 'author': '" + userInput.get() + "', 'content': '" + messageInput.get() + "'}"
        send_msg(s, content.encode('utf8'))
        messageInput.focus()

        messageInput.focus_set()
        messageInput.delete(0, length)
        # s.sendall(content.encode('utf8'))
        text['state'] = DISABLED

# text.tag_add("here", "1.0", "1.4")
# text['state'] = DISABLED
# text.tag_add("start", "1.8", "1.13")
# text.tag_config("here", background="yellow", foreground="blue")
# text.tag_config("start", background="black", foreground="green")
# text.insert(END, "Hi.....")
#
userLabel = Label(root, text='UserName')
userLabel.grid(row=1)
userInput = Entry(root)
userInput.grid(row=1, column=1, columnspan=8)

messageLabel = Label(root, text='Message')
messageLabel.grid(row=2)
messageInput = Entry(root)
messageInput.grid(row=2, column=1, columnspan=8)
postMessageBtn = Button(root, text='POST', command=postMessage)
postMessageBtn.grid(row=2, column=9)

# L1 = Label(root, text="User Name", width=15)
# L1.pack( side = LEFT)
# E1 = Entry(root, width=80)
#
# E1.pack(side = RIGHT)
# L2 = Label(root, text="Your Message", width=15)
# L2.pack()
# E2 = Entry(root, width=80)
#
# E2.pack()

receiver = receiveThread()
receiver.setDaemon(True)
receiver.start()

root.mainloop()
send_msg(s, "{'type': 'command', 'content': 'quit'}".encode('utf8'))
s.close()
