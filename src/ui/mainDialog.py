
from PyQt4.QtGui import QMainWindow
from PyQt4.QtGui import QAbstractItemView
from PyQt4.QtCore import Qt
from PyQt4 import QtCore, QtGui
from Ui_mainDialog import Ui_mainDialog
import os
import codecs
import scripts

ipTxt = "ip.txt"

class mainDialog(QMainWindow, Ui_mainDialog):
    def __init__(self, parent = None):
        
        
        QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.loadItems()
        self.loadScripts()

        
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
        file = open(ipTxt, "w")
        try:
            for i in range(self.ipList.count()):
                item = self.ipList.item(i)
                file.write(item.text() + os.linesep)
        except:
            file.close()
        
    def loadItems(self):
        file = open(ipTxt, "r")
        
        try:
            strList = file.readlines()
            self.ipList.clear()
            for string in strList:
                item = QtGui.QListWidgetItem(self.ipList)
                item.setText(string.rstrip(os.linesep))
        except:
            file.close()
            
    def getIPs(self):
        ipList = []
        for i in range(self.ipListWidget.count()):
            item = self.ipListWidget.item(i)
            ipList.append(item.text())
        return ipList
    
    def loadScripts(self):
        scriptMod = __import__('scripts')
        scriptList = []
        row = 0
        print self.tblScript.rowCount()
        for ob in dir(scriptMod):
            if (not ob.startswith('__')):
                
                self.tblScript.insertRow(row)
                
                group = (ob, getattr(scriptMod,"test").__doc__)
                print group
                
                item = QtGui.QTableWidgetItem()
                
                item.setText(str(group[0]))
                
                self.tblScript.setItem(row, 0, item)
                
                item = QtGui.QTableWidgetItem()
                item.setText(str(group[1]))
                self.tblScript.setItem(row, 1, item)
                
                row += 1
                print self.tblScript.rowCount()
        
        
        

        
    

    