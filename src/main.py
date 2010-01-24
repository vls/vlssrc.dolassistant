# -*- coding: utf-8 -*-

from dll import *
from ctypes import *
from w32 import *
import pyqmacro
from helper import *
import getopt
import client
import sys
import inspect

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import Qt, QSize
        
import ui
from ui.mainDialog import mainDialog
from ui.Ui_mainDialog import Ui_mainDialog
        
def main():
    
    
    
    opts, args = getopt.getopt(sys.argv[1:], "m:")
    
    for op, arg in opts:
        if (op == "-m"):
            if (arg == "client"):
                clientMode = True
            elif (arg == "server"):
                serverMode = True
    
    app = QtGui.QApplication(sys.argv)
    #===========================================================================
    # window = QtGui.QMainWindow()
    # uii = Ui_mainDialog()
    # 
    # uii.setupUi(window)
    #===========================================================================

    window = mainDialog()
    window.setFixedSize(QSize(424,444))
    #===========================================================================
    # item = QtGui.QListWidgetItem(window.ipList)
    # item.setText("11")
    # 
    # item = window.ipList.item(0)
    # item1 = window.ipList.item(1)
    # print item.flags().__int__()
    # print '-----'
    # item.setFlags(item.flags() | Qt.ItemFlags(Qt.ItemIsEditable))
    # print item.flags().__int__()
    # 
    # print int(window.ipList.editTriggers())
    #===========================================================================




    
    #item.setFlags(item.flags() | Qt.ItemFlags(Qt.ItemIsEditable))
    
    window.show()
    
    #===========================================================================
    # ipList = QtGui.QListWidget()
    # item = QtGui.QListWidgetItem(ipList)
    # item.setText("11")
    # item.setFlags(item.flags() | Qt.ItemFlags(Qt.ItemIsEditable))
    # item = QtGui.QListWidgetItem(ipList)
    # item.setText("22")
    # 
    # ipList.show()
    #===========================================================================
    
   
    sys.exit(app.exec_())
    
    
    
    #===========================================================================
    # print "Hello world�r��"
    # #user32.MessageBoxA(0, 'Ctypes is cool!', 'Ctypes', 0)
    # 
    # 
    # try:
    #    
    #    hWnd = win32gui.FindWindow("Greate Voyages Online Game MainFrame", None) 
    #    
    # except: 
    #    win32api.MessageBox(0, "Error",win32con.MB_ICONERROR) 
    # threadID, processID = win32process.GetWindowThreadProcessId(hWnd) 
    # hProc = OpenProcess(win32con.PROCESS_ALL_ACCESS, 0, processID) 
    # print hWnd, threadID, processID, hProc
    # 
    # helper = ProcessHelper()
    # hwnd = helper.GetMainWindowHandle(4384)
    # print hwnd
    # 
    # winHelper = WindowHelper()
    # hwndList = winHelper.GetByWindowClassName("Greate Voyages Online Game MainFrame")
    # print hwndList
    # 
    # module = __import__('scripts')
    # func = getattr(module,'test')
    # 
    # print "%d--" % len(inspect.getargspec(func)[0])
    # apply(func, [1,2])
    #===========================================================================
    


    #print pyqmacro.invoke('BGKM5.dll','KeyClick', [hWnd, 97])
    
if __name__ == "__main__":
    main()