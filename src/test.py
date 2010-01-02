# -*- coding: gbk -*-
import sys
sys.path.append("I:/document/My Documents/Visual Studio 2008/Projects/Cpp/pymemex/Debug")
import pymemex
import pyqmacro
import helper
from dol import dolScript
from ctypes import *
import time

def dowhile(callback, condition ,  args = [], interval = 0.1):
    while(condition):
        callback(*args)
        time.sleep(interval)
        
    

def main():
    hwndList = dolScript.getDolHwndList()
    #pyqmacro.dllHelp('BGKM5.dll')
    
    
    hwnd = max(hwndList)
    mxy = dolScript.getMousePos(hwnd, 0, 0)
    #pyqmacro.invoke('BGKM5.dll','LClick',[hwnd, mxy[0], mxy[1]])
   


if __name__ == "__main__":
    main()