# -*- coding: gbk -*-
import socket
import sys

from data.message_pb2 import *
from data.returnValue_pb2 import *



HOST, PORT = "localhost", 10001
class client:
    
    def __init__(self, handler):
        self.handler = handler
    
    class BaseHandler:
        def __init__(self, obj):
            try:
                self.handle(obj)
            finally:
                sys.exc_traceback = None    # Help garbage collection
        
        def handle(self, obj):
            pass
    
    def Send(self, obj):
        
        sstr = obj.SerializeToString()
        
        data = "%d,%s" % (len(sstr), sstr)
        
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
        sock.connect((HOST, PORT))
        sock.send(data)
        
        read = 0
        total = 0
        received = ""
        while (total == 0 or read < total):
            received += sock.recv(1024)
            
            
            if(total == 0):
                index = received.find(",")
                if(index != -1):
                    length = received[0:index]
                    #print length
                    total = int(length)
                    received = received[index+1:]
                      
            
            read = len(str(received))
        sock.close()
        
        recvobj = ReturnValue()
        recvobj.ParseFromString(received)
        
        returnValue = recvobj.value
        
        self.handler(returnValue)
        
        
class testHandler(client.BaseHandler):
    def handle(self, obj): 
        print obj
        
    


if __name__ ==  "__main__":
    msg = Message()
    msg.scriptName = 'test'
    
    list = ["最高神的歎息","迷途小冒險"]
    print list
    #print list[0]
    #print list[1]
    print repr(list)
    msg.playerList = repr(list)

    msg.paraList = repr(list)
    print eval(msg.playerList)
    print eval(msg.paraList)

    cl = client(testHandler)
    cl.Send(msg)

    