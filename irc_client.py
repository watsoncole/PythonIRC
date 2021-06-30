from tkinter import *
from queue import Queue
from threading import Thread
import socket as sck

class FakeConsole(Frame):
    def __init__(self, root, *args, **kargs):
        Frame.__init__(self, root, *args, **kargs)
        self.text = Text(self, bg="black", fg="white")
        self.text.pack()
        self.text.configure(state="disabled")
        self.after(5, self.on_idle)
    def on_idle(self):
        if not output_queue.empty():
            self.show(output_queue.get())
        self.after(5, self.on_idle)
    def show(self, msg):
        self.text.configure(state="normal")
        self.text.insert(END, msg)            
        self.text.see(END)
        self.text.configure(state="disabled")

class fInput(Frame):
    def __init__(self, root, *args, **kargs):
        Frame.__init__(self, root, *args, **kargs)
        self.text = Entry(self, bg="black", fg="white",width=600)
        self.text.pack()
        self.text.bind('<Return>', self.func)
        self.text.focus_force()
    def func(self,event):
        msg=self.text.get()
        message_queue.put(msg.encode('utf-8'))
        self.text.delete(0,END)

root = Tk()
root.geometry("600x406")
top=FakeConsole(root)
consoles = [top,fInput(root)]
for c in consoles:
    c.pack()
    
message_queue=Queue()
output_queue=Queue()
def fromServ(serv):
    while True:
        msg=serv.recv(1024).decode('utf-8')
        print(msg[:-1])
        output_queue.put(msg)
def toServ():
    serv = sck.socket()
    serv.connect(('localhost',1456))
    Thread(target=fromServ,args=(serv,)).start()
    while True:
        serv.send(message_queue.get())
Thread(target=toServ).start()
root.mainloop()
