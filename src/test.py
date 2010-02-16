# -*- coding: gbk -*-
import sys

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
import csv
from threadpool import ThreadPool, WorkRequest
import threading
import dol
MutexGuard = dol.global_.MutexGuard

def dountil(callback, condition ,  args = [], interval = 0.1):
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
    #ret = dll.Mouse("LClick", hwnd, 627, 495)
    #ret = dll.Key("KeyClick", hwnd, win32con.VK_RETURN)
    ret = dll.Mouse('LClick', hwnd, 547, 240)
    print ret
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


class RAII():
    def __init__(self, num):
        self.proc = num
        print 'init %d' % (self.proc)
    
    
    
    def __del__(self):
        print 'del %d' % (self.proc)   

def foo(cl):
    time.sleep(1)
    print 'foo %d' % (cl.proc)

def testRAII():
    b = RAII(99)
    for i in range(3):
        a = RAII(i)
        print a.proc
        
    print 'finish'

mutex = threading.RLock()

def rlockfunc():
    def func():
        print 'inner loop begin'
        l = MutexGuard(mutex)
        #time.sleep(0.5)
        print 'inner loop end'
    
    for i in range(3):
        while(True):
            
            func()
            
            
            break
        #time.sleep(0.5)
        #print 'explict release'
        #l.__del__()
        print 'outter loop end'

def testRlock():
    l = MutexGuard(mutex)
    print 'testRlock() acquired'
    rlockfunc()
    
def main2():
    wri = csv.writer(open('test.csv', 'w'))
    strList = [('123', 456, 'sss')]
    
    wri.writerows(strList)

if __name__ == "__main__":
    testRlock()