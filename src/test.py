# -*- coding: gbk -*-
import sys
sys.path.append("I:/document/My Documents/Visual Studio 2008/Projects/Cpp/pymemex/Debug")
import pymemex
import pyqmacro
import helper
import dolScript
from ctypes import *

def main():
    hwndList = dolScript.getDolHwndList()
    #pyqmacro.dllHelp('BGKM5.dll')
    
    mxy = (1152 - 171 + 36 /2 , 864 - 251 + 20 /2)
    hwnd = max(hwndList)
    pyqmacro.invoke('BGKM5.dll','LClick',[hwnd, mxy[0], mxy[1]])
    
    
    print hwndList

if __name__ == "__main__":
    main()