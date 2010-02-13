# -*- coding: utf-8 -*-

import time, datetime
from ctypes import windll, byref
from ctypes import c_wchar_p, c_ulong, c_char_p, c_ubyte, c_uint, c_float, c_int
import win32api, win32con
import traceback
import sys
import os
sys.path.append("..")



class MyList(list):
    def __str__(self):
        str = ''
        for x in self:
            str += repr(x)
            str += ', '
        return '[%s]' % (str[:-2])



kernel32 = windll.kernel32
VirtualAllocEx = kernel32.VirtualAllocEx
VirtualFreeEx = kernel32.VirtualFreeEx
LoadLibraryA = kernel32.LoadLibraryA
WriteProcessMemory = kernel32.WriteProcessMemory

def dountil(func, args = None, interval = 0.2):
    if(args == None):
        args = []
    while(not func(*args)):
        time.sleep(interval)
        
def dowhile(func, args = None, interval = 0.2):
    if(args == None):
        args = []
    while(func(*args)):
        time.sleep(interval)
        
        
def getStringW(proc, addr, length):
    buf = c_wchar_p(' ' * (length))
    bytesRead = c_ulong(0)
    kernel32.ReadProcessMemory(proc.handle, addr, buf, length * 2, byref(bytesRead))
    return buf.value

def getString(proc, addr, length):
    buf = c_char_p(' ' * (length * 2))
    bytesRead = c_ulong(0)
    kernel32.ReadProcessMemory(proc.handle, addr, buf, length * 2, byref(bytesRead))
    return buf.value

def getInt(proc, addr):
    '''获取4字节的内容
        return int
    '''
    buf = c_uint(0)
    bytesRead = c_ulong(0)
    bufferSize = 4    
    kernel32.ReadProcessMemory(proc.handle, addr, byref(buf), bufferSize, byref(bytesRead))
    return buf.value

def getShort(proc, addr):
    '''获取两字节内容
        return short int
    '''
    buf = c_int(0)
    bytesRead = c_ulong(0)
    bufferSize = 2    
    kernel32.ReadProcessMemory(proc.handle, addr, byref(buf), bufferSize, byref(bytesRead))
    return buf.value

def getByte(proc, addr):
    buf = c_ubyte()
    bytesRead = c_ulong(0)
    bufferSize = 1    
    kernel32.ReadProcessMemory(proc.handle, addr, byref(buf), bufferSize, byref(bytesRead))
    return buf.value

def getFloat(proc, addr):
    '''获取float
        return float
    '''
    buf = c_float(0)
    bytesRead = c_ulong(0)
    bufferSize = 8    
    kernel32.ReadProcessMemory(proc.handle, addr, byref(buf), bufferSize, byref(bytesRead))
    return buf.value


def log(msg):
    print "%s : %s " % (datetime.datetime.now(), msg)
    
class TextLogger():
    def __init__(self, filename):
        self.filename = filename
        self.writer = open(filename, 'a')
        print self.writer
         
    def __del__(self):
        self.writer.close()
    
    def log(self, msg):
        msglog = "%s : %s " % (datetime.datetime.now(), msg)
        print msglog
        self.writer.write(msglog + os.linesep)
        self.writer.flush()

def msgBox(title = "", message = ""):
    try:
        win32api.MessageBox(None, message.decode('utf-8'), title.decode('utf-8'), win32con.MB_ICONINFORMATION | win32con.MB_TOPMOST)
    except UnicodeDecodeError, e:
        traceback.print_exc(file=sys.stdout)
        win32api.MessageBox(None, "Something wrong !!! (Please check the encoding of the file who raise the *beep*)", "Warning", win32con.MB_ICONERROR | win32con.MB_TOPMOST)
    
    
def beep(title = "", message = ""):
    for i in range(3):
        win32api.MessageBeep(win32con.MB_ICONEXCLAMATION)
        time.sleep(0.5)
    try:
        win32api.MessageBox(None, message.decode('utf-8'), title.decode('utf-8'), win32con.MB_ICONERROR | win32con.MB_TOPMOST)
    except UnicodeDecodeError, e:
        traceback.print_exc(file=sys.stdout)
        win32api.MessageBox(None, "Something wrong !!! (Please check the encoding of the file who raise the *beep*)", "Warning", win32con.MB_ICONERROR | win32con.MB_TOPMOST)

def main():
    logger = TextLogger('test.txt')
    logger.log('123')

if __name__ == "__main__":
    main()   
