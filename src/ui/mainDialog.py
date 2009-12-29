
from PyQt4.QtGui import QMainWindow
from PyQt4.QtGui import QAbstractItemView
from PyQt4.QtCore import Qt
from Ui_mainDialog import Ui_mainDialog


class mainDialog(QMainWindow, Ui_mainDialog):
    def __init__(self, parent = None):
        QMainWindow.__init__(self, parent)
        self.setupUi(self)
        item = self.ipList.item(0)
        item1 = self.ipList.item(1)
        print item.flags().__int__()
        print int(item1.flags())
        print '-----'
        item.setFlags(item.flags() | Qt.ItemFlags(Qt.ItemIsEditable))
        print item.flags().__int__()
        print int(item1.flags())
        
        print int(self.ipList.editTriggers())
        
    def test(self, item):
        print 'clicked'
        self.ipList.editItem(item)
        
    

    