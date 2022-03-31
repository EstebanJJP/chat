from multiprocessing.connection import Client
from random import random
from time import sleep

from multiprocessing.connection import Listener
from multiprocessing import Process

local_listener = (('127.0.0.1', 5001),b'secret client password')

def client_listener():
    cl = Listener(address = local_listener[0], authkey = local_listener[1])
    print ('.............client listener starting') 
    print ('.............accepting conexions')
    while True:
        conn = cl.accept()
        print ('.............connection accepted from', cl.last_accepted)       
        m = conn.recv()
        print ('.............message received from server', m)


if __name__ == '__main__':

    print ('trying to connect')
    conn = Client(address=('127.0.0.1', 6000), authkey=b'secret password server')
    conn.send(local_listener)

    cl = Process(target = client_listener, args = ())
    cl.start()
    
    connected = True
    while connected:
        value = input("Send message ('Q' quit connection)?")
        if value == 'Q':
            connected = False
        else:
            print ("connection continued...")
            conn.send("connected")
        
    print ("last message")
    conn.send("quit")
    conn.close()
    cl.terminate()
    print ("end client")
