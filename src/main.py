# -*- coding: gb2312 -*-

from dll import *
from ctypes import *
import pyqmacro
import win32process
import win32gui
import win32con
import win32api
 
kernel32 = windll.LoadLibrary("kernel32.dll") 
ReadProcessMemory = kernel32.ReadProcessMemory 
WriteProcessMemory = kernel32.WriteProcessMemory 
OpenProcess = kernel32.OpenProcess 

        
def main():
    print "Hello world"
    #user32.MessageBoxA(0, 'Ctypes is cool!', 'Ctypes', 0)
    
    
    try: 
        hWnd = win32gui.FindWindow("Notepad", None) 
    except: 
        win32api.MessageBox(0, "请先运行扫雷程序", "错误！", win32con.MB_ICONERROR) 
    threadID, processID = win32process.GetWindowThreadProcessId(hWnd) 
    hProc = OpenProcess(win32con.PROCESS_ALL_ACCESS, 0, processID) 
    print hWnd, threadID, processID, hProc

        
    print pyqmacro.invoke('GetSysInfo.dll','abc', ['list1', 'list2'])
    
if __name__ == "__main__":
    main()