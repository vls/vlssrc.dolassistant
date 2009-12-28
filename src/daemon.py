
import SocketServer
from data import message_pb2 
from datetime import datetime

class ListenTCPHandler(SocketServer.BaseRequestHandler):
    def handle(self):
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
        

        msg = message_pb2.Message()
        #print "After read..."
        #print "read = %d, total = %d" % (read,total)
        #print self.data
        msg.ParseFromString(self.data)
        #print "After decode..."
        print datetime.now()
        print msg
        
        list = eval(msg.playerList)
        paraList = eval(msg.paraList)
        
        execScript(msg.scriptName, paraList)
        
        

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
    apply(func, paraList)
    
if __name__ == "__main__":
    start()