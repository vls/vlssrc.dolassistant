import win32process
import win32gui
import win32con
import win32api
from ctypes import *


class w32:
    
 
    kernel32 = windll.kernel32 
    ReadProcessMemory = kernel32.ReadProcessMemory 
    WriteProcessMemory = kernel32.WriteProcessMemory 
    OpenProcess = kernel32.OpenProcess 
    
    user32 = windll.user32
    
    
    @staticmethod
    def ReadMemEx(proc, addrList, bufAddr, bufferSize, readAddr):
        if(len(addrList) == 0):
            return
        w32.ReadProcessMemory(proc, addrList[0], bufAddr._obj, bufferSize, readAddr)
        print bufAddr._obj
        for i in range(1,len(addrList)):
            print dir(bufAddr)
            w32.ReadProcessMemory(proc, bufAddr._obj.value + addrList[i], bufAddr, bufferSize, readAddr)