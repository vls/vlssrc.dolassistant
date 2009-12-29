from PyQt4 import QtCore
from PyQt4.QtCore import QVariant


class stringListModel(QtCore.QAbstractListModel):
    def __init__(self, parent = None):
        QtCore.QAbstractListModel.__init__(self, parent)
        self.stringList = []
        
    def rowCount(self, parent = QtCore.QModelIndex()):
        return len(self.stringList)
    
    def data(self, index, role = QtCore.Qt.DisplayRole):
        if(not index.isValid()):
            return QVariant()
        
        if(index.row() >= len(self.stringList)):
            return QVariant()
        
        if(role == QtCore.Qt.DisplayRole):
            return self.stringList[index.row()]
        else:
            return QVariant()
        
        