""" Message Listening Daemon class 
"""
import SocketServer
from data.message_pb2 import Message 
from data.returnValue_pb2 import ReturnValue 
from datetime import datetime

class ListenTCPHandler(SocketServer.BaseRequestHandler):
    """ a handler to listen, process, send back 
    """
    def handle(self):
        """ overriding the function of super class
        """
        self.data = ""
        read = 0
        total = 0
        while (total == 0 or read < total):
            self.data += self.request.recv(1024)
            #print self.data
            
            if(total == 0):
                index = self.data.find(",")
                if(index != -1):
                    length = self.data[0:index]
                    #print length
                    total = int(length)
                    self.data = self.data[index+1:]
                      
            
            read = len(str(self.data))
        

        msg = Message()
        #print "After read..."
        #print "read = %d, total = %d" % (read,total)
        #print self.data
        msg.ParseFromString(self.data)
        #print "After decode..."
        print datetime.now()
        print msg
        
        plList = eval(msg.playerList)
        paraList = eval(msg.paraList)
        
        rt = execScript(msg.scriptName, paraList)
        
        sstr = rt.SerializeToString()
        
        data = "%d,%s" % (len(sstr), sstr)
        
        self.request.send(data)
        
        

HOST, PORT = "localhost", 10001
server = SocketServer.TCPServer((HOST, PORT), ListenTCPHandler)

def start():   
    
    
    print "Starting"
    server.serve_forever()
    print "Started"
    
def stop():
    server.shutdown()
    
    
def execScript(scriptName, paraList):
    module = __import__('scripts')
    func = getattr(module, scriptName)    
    retvalue = func(*paraList)
    
    rt = ReturnValue()
    rt.value = repr(retvalue)
    
    return rt
    
if __name__ == "__main__":
    start()