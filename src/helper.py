
import pywintypes
from win32 import win32gui, win32process, win32api, win32con
import os
import winnt

class ProcessHelper:
    
    
    def IsMainWindow(self, handle):
        flag1 = (win32gui.GetWindow(handle, 4) != 0)
        flag2 = win32gui.IsWindowVisible(handle)
        result =  (not flag1) and flag2
        return result
    
    def callback(self, hwnd, extra):
        threadID, procID = win32process.GetWindowThreadProcessId(hwnd)
        #print threadID, procID, hwnd
        if ((procID == self.processID) and self.IsMainWindow(hwnd)):
            self.mainWindowHandle = hwnd
            return False
        return True
        
    def GetMainWindowHandle(self, processID):
        self.processID = processID
        self.mainWindowHandle = 0
        try:
            win32gui.EnumWindows(self.callback, 0)
        except pywintypes.error as e:
            if(win32api.GetLastError() != 0):
                raise e
            
        return self.mainWindowHandle
    
    
        
    
class WindowHelper:
    def getWindowListByClassName(self, className):
        self.className = className
        self.hwndList = []
        self.mainWindowHandle = 0
        try:
            win32gui.EnumWindows(self.classNameCallback, 0)
        except pywintypes.error as e:
            if(win32api.GetLastError() != 0):
                raise e
            
        return self.hwndList
    
    def classNameCallback(self, hwnd, extra):
        className = win32gui.GetClassName(hwnd)
        #print hwnd, className
        if(className == self.className):
            self.hwndList.append(hwnd)
        return True
    
    
    def getProcListByClassName(self, className):
        
        hwndList = self.getWindowListByClassName(className)
        
        procList = []
        
        for hwnd in hwndList:
            threadID, processID = win32process.GetWindowThreadProcessId(hwnd) 
            hProc = win32api.OpenProcess(win32con.PROCESS_ALL_ACCESS, 0, processID)
            procList.append(hProc)
            
        return procList
        
        