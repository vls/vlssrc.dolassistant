# -*- coding: gbk -*-
import sys
sys.path.append("I:/document/My Documents/Visual Studio 2008/Projects/Cpp/pymemex/Debug")
import pymemex
import pyqmacro
import helper
from dol import dolScript
from ctypes import *
import time
import dll
from helper import WindowHelper
import win32con
import win32gui
import win32api

def dowhile(callback, condition ,  args = [], interval = 0.1):
    while(condition):
        callback(*args)
        time.sleep(interval)
        
    

def main():
    hwndList = dolScript.getDolHwndList()
    #pyqmacro.dllHelp('BGKM5.dll')
    
    print hwndList
    hwnd = hwndList[0]
    proc = WindowHelper.getProcByHwnd( hwnd)
    print dolScript.getRoleName(proc)
    
    
    mxy = dolScript.getMousePos(hwnd, 0, 0)
    #pyqmacro.invoke('BGKM5.dll','LClick',[hwnd, mxy[0], mxy[1]])
    #ret = dll.Mouse("LClick", hwnd, 200, 200)
    ret = dll.Key("KeyClick", hwnd, 0x1b)

    print win32gui.SetActiveWindow(hwnd)
    print win32api.GetLastError()
    #print windll.user32.PostMessageA(hwnd, win32con.WM_KEYDOWN, 9,0x1)
    #time.sleep(0.01)
    #print windll.user32.PostMessageA(hwnd, win32con.WM_CHAR, 13,0)
    
    #print windll.user32.PostMessageA(hwnd, win32con.WM_KEYUP, 9,0xC0000001)
    #print windll.user32.PostMessageA(hwnd, win32con.WM_KEYDOWN, 13,0x1C0001)
    time.sleep(0.01)
    #print windll.user32.PostMessageA(hwnd, win32con.WM_CHAR, 13,0x1)
    time.sleep(0.01)
    #print windll.user32.PostMessageA(hwnd, win32con.WM_KEYUP, 13,0xC01C0001)
   


if __name__ == "__main__":
    main()