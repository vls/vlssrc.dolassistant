
import pywintypes
import win32gui, win32process, win32api, win32con
import os
import winnt
import datetime


class ProcessHelper:
    
    
    def isMainWindow(self, handle):
        flag1 = (win32gui.GetWindow(handle, 4) != 0)
        flag2 = win32gui.IsWindowVisible(handle)
        result =  (not flag1) and flag2
        return result
    
    def callback(self, hwnd, extra):
        threadID, procID = win32process.GetWindowThreadProcessId(hwnd)
        #print threadID, procID, hwnd
        if ((procID == self.processID) and self.isMainWindow(hwnd)):
            self.mainWindowHandle = hwnd
            return False
        return True
        
    def getMainWindowHandle(self, processID):
        self.processID = processID
        self.mainWindowHandle = 0
        try:
            win32gui.EnumWindows(self.callback, 0)
        except pywintypes.error, e:
            if(win32api.GetLastError() != 0):
                raise e
            
        return self.mainWindowHandle
    
    def getHwndByProc(self, proc):
        pid = win32process.GetProcessId(proc)
        return self.getMainWindowHandle(pid)
    
        
    
class WindowHelper:
    def getWindowListByClassName(self, className):
        self.className = className
        self.hwndList = []
        self.mainWindowHandle = 0
        try:
            win32gui.EnumWindows(self.classNameCallback, 0)
        except pywintypes.error, e:
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
        #print hwndList
        for hwnd in hwndList:
            threadID, processID = win32process.GetWindowThreadProcessId(hwnd) 
            hProc = win32api.OpenProcess(win32con.PROCESS_ALL_ACCESS, 0, processID)
            procList.append(hProc)
            
        return procList
    
    @staticmethod
    def getProcByHwnd(hwnd):
        threadID, processID = win32process.GetWindowThreadProcessId(hwnd) 
        hProc = win32api.OpenProcess(win32con.PROCESS_ALL_ACCESS, 0, processID)
        return hProc

class ProcGuard:
    def __init__(self, hwnd):
        threadID, processID = win32process.GetWindowThreadProcessId(hwnd) 
        self.proc = win32api.OpenProcess(win32con.PROCESS_ALL_ACCESS, 0, processID)
        self.seq = self.proc.handle
        #print '%s : open process %d' % (datetime.datetime.now(), self.seq)
    
    def __del__(self):
        ret = win32api.CloseHandle(self.proc)
        if(ret == 0):
            print 'Close fail. Error = %d' % (win32api.GetLastError())
        