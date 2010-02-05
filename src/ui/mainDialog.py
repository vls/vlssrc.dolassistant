# -*- coding: utf-8 -*-
import sys
sys.path.append("..")
from global_ import reloadMod
from PyQt4.QtGui import QMainWindow
from PyQt4.QtGui import QAbstractItemView
from PyQt4.QtCore import Qt
from PyQt4 import QtCore, QtGui
from Ui_mainDialog import Ui_mainDialog
import os
import codecs
import scripts
import types
import threadpool
from threadpool import ThreadPool, makeRequests, WorkRequest
from client import client
import mainDialogBL
import win32con
from w32 import w32
import inspect
from ctypes import *
from global_ import *

def MessageBox(hwnd, string, caption, flag):
    string = string.decode('utf-8')
    caption = caption.decode('utf-8')
    windll.user32.MessageBoxW(hwnd, string, caption, flag)
        

class playerListHandler(client.BaseHandler):
    def handle(self, obj):
        pass

class mainDialog(QMainWindow, Ui_mainDialog):
    
    ipTxt = "ip.txt"
    keyTxt = "key.txt"
    
    def write(self, s):
        self.txt.appendPlainText(s.rstrip(os.linesep))
    
    def __init__(self, parent = None):
        
        
        QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)
        #self.addContextMenu()
        
        self.stdout_ = sys.stdout
        #sys.stdout = self
        
        self.flagRun = True
        
        self.loadItems()
        self.loadScripts()
        self.pool = ThreadPool(6)
        self.keyDict = {}
        self.loadKey(self.keyTxt)
        self.autoRegKey()
        
        
        
        self.txt.appendPlainText("123")
        self.txt.appendPlainText("123456")
        #w32.user32.RegisterHotKey(self.winId().__int__(), 5555, win32con.MOD_ALT, ord("1"))
        
        #print "reg = %d" % ( w32.user32.RegisterHotKey(self.winId().__int__(), 4444, win32con.MOD_WIN, win32con.VK_F3))
        
#===============================================================================
# private functions
#===============================================================================
    def addContextMenu(self):
        '''
        增加右键菜单
        '''
        action = QtGui.QAction(unicode('总在最前'), self)
        action.setCheckable(True)
        self.connect(action, QtCore.SIGNAL("toggled(bool)"), self.topToggled)
        
        self.addAction(action)
    
    


        
    def loadItems(self):
        try:
            file = open(self.ipTxt, "r")
        except IOError:
            return
        
        try:
            strList = file.readlines()
            self.ipListWidget.clear()
            for string in strList:
                item = QtGui.QListWidgetItem(self.ipListWidget)
                item.setText(string.rstrip(os.linesep))
        finally:
            file.close()
            
    def getIPs(self):
        ipList = []
        for i in range(self.ipListWidget.count()):
            item = self.ipListWidget.item(i)
            ipList.append(item.text())
        return ipList
    
    def loadScripts(self):
        scriptMod = reloadMod('scripts')
        scriptList = []
        row = 0
        #print self.tblScript.rowCount()
        for ob in dir(scriptMod):
            if (not ob.startswith('__') and type(getattr(scriptMod, ob)) == types.FunctionType):
                
                self.tblScript.insertRow(row)
                doc = getattr(scriptMod,ob).__doc__
                
                
                docStr = ""
                if(doc != None):
                    #docStr = doc
                    #print dir(QtGui.QApplication)
                    doc = doc.strip()
                    docStr = QtGui.QApplication.translate("mainDialog", doc, None, QtGui.QApplication.UnicodeUTF8)
                
                group = (ob, docStr)
                #print group
                
                item = QtGui.QTableWidgetItem()
                item.setText(group[0])
                item.setFlags(item.flags() & ~Qt.ItemFlag(Qt.ItemIsEditable))
                
                self.tblScript.setItem(row, 0, item)
                
                item = QtGui.QTableWidgetItem()
                item.setText(group[1])
                item.setFlags(item.flags() & ~Qt.ItemFlag(Qt.ItemIsEditable))
                
                self.tblScript.setItem(row, 1, item)
                
                row += 1
                #print self.tblScript.rowCount()
                
                

    

    
    def execScript(self):

        hwndList = self.getPlayerHwndList()
        
        if(len(hwndList) == 0):
            MessageBox(0, "请选择要发送命令的窗口", "", 0)
            return
        
        itemList =  self.tblScript.selectedItems()
        
        if(len(itemList) == 0):
            print "no selected row"
            return
        
        item = itemList[0]
        row = self.tblScript.row(item)
        item = self.tblScript.item(row, 0)
            
        txt = str(item.text()).strip()
        
        self.invokeScript(txt)
        
    
    def loadKey(self, filename):
        
        kDict = {}
        
        rowCount = self.tblScript.rowCount()
        for row in range(rowCount):
            item = self.tblScript.item(row, 0)
            
            txt = str(item.text()).strip()
            if(not kDict.has_key(txt)):
                kDict[txt] = self.tblScript.row(item)
        
        #print kDict
        
        file = None
        try:
            file = open(filename, "r")
        except IOError:
            return
            
        try:
            strList = file.readlines()
            for string in strList:
                string = string.rstrip(os.linesep)
                splitStr = string.split(",", 1)
                name = splitStr[0].strip()
                if(kDict.has_key(name)):
                    item = QtGui.QTableWidgetItem()
                    key = splitStr[1].strip()[:1]
                    item.setText(key)
                    self.tblScript.setItem(kDict[name], 2, item)
                    
                    
            print "Load %s for key completed" % (filename)    
        finally:
            file.close()
    
    def saveKey(self, filename):
        file = open(filename, "w")
        
        kDict = {}
        
        rowCount = self.tblScript.rowCount()
        for row in range(rowCount):
            name = str(self.tblScript.item(row, 0).text()).strip()
            item = self.tblScript.item(row, 2)
            if(not (item == None or item.text().length() == 0)):
                key = str(self.tblScript.item(row, 2).text()).strip()[:1]
                if(not kDict.has_key(key)):
                    kDict[key] = name
                    file.write("%s,%s" % (name, key) + os.linesep)
                else:
                    
                    self.tblScript.takeItem(row, 2)
    
    def regKey(self):
        for k,v in self.keyDict.items():
            #print v
            w32.user32.RegisterHotKey(self.winId().__int__(), k, win32con.MOD_ALT, ord(v[0]))
    
    def generateKeyDict(self):
        self.keyDict.clear()
        kDict = {}
        id = 1
        rowCount = self.tblScript.rowCount()
        for row in range(rowCount):
            name = str(self.tblScript.item(row, 0).text()).strip()
            item = self.tblScript.item(row, 2)
            if(not (item == None or item.text().length() == 0)):
                key = str(item.text()).strip()[:1]
                if(not kDict.has_key(key)):
                    kDict[key] = name
                    self.keyDict[id] = (key, name)
                    id += 1
            
    def unRegKey(self):
        for k,v in self.keyDict.items():
            w32.user32.UnregisterHotKey(self.winId().__int__(), k)
    
    def autoRegKey(self):
        self.unRegKey()
        self.generateKeyDict()
        self.regKey()
        
    def invokeScript(self, funcName):
        module = reloadMod('scripts')
        func = getattr(module, funcName)
        self.flagRun = True
        module.window = self
        
        args, varargs, varkw, defaults = inspect.getargspec(func)        
        
        if(len(args) < 2):
            MessageBox(0, "脚本参数个数少于2", "", 0)
            return
        
        hwndList = self.getPlayerHwndList()
        
        
        
        if(len(hwndList) == 0):
            MessageBox(0, "请选择要发送命令的窗口", "", 0)
            return
        
        

        prefunc = None
        try:
            prefunc = getattr(module, "__%s_pre" % (funcName))
        except AttributeError as e:
            pass
            
        if(prefunc != None):
            flag, preargs = prefunc(self)
            
        if(prefunc != None and not flag):
            return
        
        requests = []
        
        for hwnd in hwndList:
            if(prefunc != None):
                print preargs
                re = WorkRequest(mainDialogBL.scriptWrap, [func, hwnd, list(preargs)])
                self.pool.putRequest(re)
                
            else:
                re = WorkRequest(mainDialogBL.scriptWrap, [func, hwnd, []])
                print "In invokeScript(): args = %s" % (re.args)
                self.pool.putRequest(re)
            
        
    

        
         
#===============================================================================
# Slot           
#===============================================================================
    def topToggled(self, flag):
        print self.winId()
        if(flag):
            self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)
        else:
            self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowStaysOnTopHint)
        self.show()
        print self.winId()

    def saveScript(self):
        self.saveKey(self.keyTxt)
        self.autoRegKey()
        
        
    
    def refreshScript(self):
        self.tblScript.setRowCount(0)
        self.loadScripts()
        self.tblScript.sortItems(0)
        self.loadKey(self.keyTxt)
        self.autoRegKey()
    
            
    def addItem(self):
        item = QtGui.QListWidgetItem(self.ipListWidget)
        item.setFlags(item.flags() | Qt.ItemFlag(Qt.ItemIsEditable))
        self.ipListWidget.editItem(item)    

    def deleteItem(self):
        #print self.ipListWidget.count()
        
        itemList =  self.ipListWidget.selectedItems()
        for item in itemList:
            self.ipListWidget.takeItem(self.ipListWidget.row(item))
        
        self.ipListWidget.setCurrentItem(None)
        #print self.ipListWidget.count()

        
    def saveItems(self):
        file = open(self.ipTxt, "w")
        try:
            for i in range(self.ipList.count()):
                item = self.ipList.item(i)
                file.write(item.text() + os.linesep)
        finally:
            file.close()
            
    def setPlayerList(self):
        infoList = mainDialogBL.getDolList()
        self.tblPlayer.setRowCount(0)
        row = 0
        for info in infoList:
            self.tblPlayer.insertRow(row)
            
            item = QtGui.QTableWidgetItem()
            item.setText(info[0])
            self.tblPlayer.setItem(row, 0, item)
            
            item = QtGui.QTableWidgetItem()
            item.setText(str(info[1]))
            self.tblPlayer.setItem(row, 1, item)
            
            item = QtGui.QTableWidgetItem()
            item.setText(str(info[2]))
            self.tblPlayer.setItem(row, 2, item)
            
            row += 1
    
    def wiseMin(self):
        mainDialogBL.wiseMin(self.getPlayerHwndList())
            
    def stopScript(self):
        self.flagRun = False
        self.pool.workRequests.clear()
    
    
#===============================================================================
# Event
#===============================================================================
        
    def winEvent(self, msg):       
        #print msg.message
        #print msg.wParam
        if(msg.message == win32con.WM_HOTKEY):
            print "hotkey %d" % (msg.wParam)
            if(self.keyDict.has_key(msg.wParam)):
                name = self.keyDict[msg.wParam][1]
                self.invokeScript(name)
        return False, id(msg)
    
    def closeEvent(self, event):
        #print "unreg=%d" % ( w32.user32.UnregisterHotKey(self.winId().__int__(), 4444))
        self.pool.wait()
        print "close"
        #event.accept()
        
    
#---------------------------------------------------------
#---------------------------------------------------------
#---------------------------------------------------------
#---------------------------------------------------------         
    def getPlayerHwndList(self):
        hwndList = []

        for row in range(self.tblPlayer.rowCount()):
            item = self.tblPlayer.item(row, 1)
            if(item.isSelected()):
                hwnd = item.text().toInt()[0]
                hwndList.append(hwnd)
        return hwndList
    
    
    
    
    
    
    

        
    
    
    
        


        
        

        
    
