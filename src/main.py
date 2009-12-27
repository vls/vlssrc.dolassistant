# -*- coding: GBK -*-

from dll import *
from ctypes import *
from win32 import *
import pyqmacro
from helper import *


        
    
        
def main():
    print "Hello world時代"
    #user32.MessageBoxA(0, 'Ctypes is cool!', 'Ctypes', 0)
    
    
    try:
        
        hWnd = win32gui.FindWindow("Greate Voyages Online Game MainFrame", None) 
        
    except: 
        win32api.MessageBox(0, "Error",win32con.MB_ICONERROR) 
    threadID, processID = win32process.GetWindowThreadProcessId(hWnd) 
    hProc = OpenProcess(win32con.PROCESS_ALL_ACCESS, 0, processID) 
    print hWnd, threadID, processID, hProc
    
    helper = ProcessHelper()
    hwnd = helper.GetMainWindowHandle(4384)
    print hwnd
    
    winHelper = WindowHelper()
    hwndList = winHelper.GetByWindowClassName("Greate Voyages Online Game MainFrame")
    print hwndList
    
    


    #print pyqmacro.invoke('BGKM5.dll','KeyClick', [hWnd, 97])
    
if __name__ == "__main__":
    main()