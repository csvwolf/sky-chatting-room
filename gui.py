from Tkinter import *
import socket
import threading

root = Tk()
text = Text(root)
text.insert(INSERT, "Hello.....")
text.insert(END, "Bye Bye.....")
text.grid(row = 0, columnspan=15)

s = socket.socket()

host = socket.gethostname()
port = 1234
status = True
s.connect((host, port))

class receiveThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        while 1:
            word = s.recv(1024)
            if (word):
                text['state'] = NORMAL
                text.insert(END, '\n' + word)
                text['state'] = DISABLED

def postMessage():
    text['state'] = NORMAL
    text.insert(END, '\n' + userInput.get() + ': ' + messageInput.get())
    s.sendall(userInput.get() + ': ' + messageInput.get())
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

receiveThread().start()

root.mainloop()

s.close()
