
import pywintypes
from win32 import *

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
    def GetByWindowClassName(self, className):
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