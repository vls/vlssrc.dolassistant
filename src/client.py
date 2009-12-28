# -*- coding: gbk -*-
import socket
import sys

from data import message_pb2



HOST, PORT = "localhost", 10001

def Send(obj):
    
    sstr = obj.SerializeToString()
    
    data = "%d,%s" % (len(sstr), sstr)
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    sock.connect((HOST, PORT))
    sock.send(data)



if __name__ ==  "__main__":
    msg = message_pb2.Message()
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

    Send(msg)