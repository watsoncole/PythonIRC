from queue import Queue
from threading import Thread
import socket as sck

message_queue=Queue()
output_queue=Queue()
relay_list=[]
def out(*arg):
    output_queue.put(arg)
def print_out():
    while True:
        print(*(output_queue.get()))
              
def relay():
    while True:
        current = message_queue.get()
        for con in relay_list:
            try:
                con.send(current.encode('utf-8'))
            except:
                out('Disconnected2:')
                con.close()
                relay_list.remove(con)
                break

def wait(con,addr):
    out('Connected:',addr)
    relay_list.append(con)
    message_queue.put(str(addr)+' Connected'+'\n')
    while True:
        try:
            data=con.recv(1024).decode('utf-8')
            if '' == data:
                DSFDSFSF=5/0
            msg = str(addr)+': '+data
            message_queue.put(msg+'\n')
            out(msg)
        except:
            out('Disconnected:',addr)
            message_queue.put(str(addr)+' Disconnected'+'\n')
            relay_list.remove(con)
            con.close()
            break

def bind(*arg):
    serv = sck.socket()
    serv.bind(arg)
    while True:
        serv.listen(5)
        Thread(target=wait,args=serv.accept()).start()
        
Thread(target=bind,args=('localhost',1456)).start()
Thread(target=relay).start()
print_out()
