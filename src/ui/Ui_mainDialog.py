# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainDialog.ui'
#
# Created: Tue Dec 29 19:52:03 2009
#      by: PyQt4 UI code generator 4.6.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_mainDialog(object):
    def setupUi(self, mainDialog):
        mainDialog.setObjectName("mainDialog")
        mainDialog.resize(425, 450)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(mainDialog.sizePolicy().hasHeightForWidth())
        mainDialog.setSizePolicy(sizePolicy)
        mainDialog.setAutoFillBackground(False)
        self.tabWidget = QtGui.QTabWidget(mainDialog)
        self.tabWidget.setGeometry(QtCore.QRect(10, 10, 401, 431))
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtGui.QWidget()
        self.tab.setObjectName("tab")
        self.tblPlayer = QtGui.QTableWidget(self.tab)
        self.tblPlayer.setGeometry(QtCore.QRect(10, 10, 369, 165))
        self.tblPlayer.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.tblPlayer.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tblPlayer.setShowGrid(True)
        self.tblPlayer.setGridStyle(QtCore.Qt.SolidLine)
        self.tblPlayer.setObjectName("tblPlayer")
        self.tblPlayer.setColumnCount(3)
        self.tblPlayer.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.tblPlayer.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tblPlayer.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.tblPlayer.setHorizontalHeaderItem(2, item)
        self.tblScript = QtGui.QTableWidget(self.tab)
        self.tblScript.setGeometry(QtCore.QRect(10, 210, 369, 141))
        self.tblScript.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.tblScript.setObjectName("tblScript")
        self.tblScript.setColumnCount(3)
        self.tblScript.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.tblScript.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tblScript.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.tblScript.setHorizontalHeaderItem(2, item)
        self.btnExec = QtGui.QPushButton(self.tab)
        self.btnExec.setGeometry(QtCore.QRect(220, 360, 161, 41))
        self.btnExec.setObjectName("btnExec")
        self.btnSaveScript = QtGui.QPushButton(self.tab)
        self.btnSaveScript.setGeometry(QtCore.QRect(10, 360, 80, 25))
        self.btnSaveScript.setObjectName("btnSaveScript")
        self.btnRefresh = QtGui.QPushButton(self.tab)
        self.btnRefresh.setGeometry(QtCore.QRect(10, 180, 80, 25))
        self.btnRefresh.setObjectName("btnRefresh")
        self.progLoad = QtGui.QProgressBar(self.tab)
        self.progLoad.setGeometry(QtCore.QRect(240, 180, 118, 23))
        self.progLoad.setProperty("value", 0)
        self.progLoad.setObjectName("progLoad")
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.btnAdd = QtGui.QPushButton(self.tab_2)
        self.btnAdd.setGeometry(QtCore.QRect(10, 370, 75, 23))
        self.btnAdd.setObjectName("btnAdd")
        self.btnDelete = QtGui.QPushButton(self.tab_2)
        self.btnDelete.setGeometry(QtCore.QRect(90, 370, 75, 23))
        self.btnDelete.setObjectName("btnDelete")
        self.btnSave = QtGui.QPushButton(self.tab_2)
        self.btnSave.setGeometry(QtCore.QRect(170, 370, 75, 23))
        self.btnSave.setObjectName("btnSave")
        self.ipListWidget = QtGui.QListWidget(self.tab_2)
        self.ipListWidget.setGeometry(QtCore.QRect(10, 10, 371, 351))
        self.ipListWidget.setObjectName("ipListWidget")
        self.tabWidget.addTab(self.tab_2, "")

        self.retranslateUi(mainDialog)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QObject.connect(self.btnAdd, QtCore.SIGNAL("clicked()"), mainDialog.addItem)
        QtCore.QObject.connect(self.btnDelete, QtCore.SIGNAL("clicked()"), mainDialog.deleteItem)
        QtCore.QObject.connect(self.btnSave, QtCore.SIGNAL("clicked()"), mainDialog.saveItems)
        QtCore.QMetaObject.connectSlotsByName(mainDialog)

    def retranslateUi(self, mainDialog):
        mainDialog.setWindowTitle(QtGui.QApplication.translate("mainDialog", "控制端", None, QtGui.QApplication.UnicodeUTF8))
        self.tblPlayer.setSortingEnabled(True)
        self.tblPlayer.horizontalHeaderItem(0).setText(QtGui.QApplication.translate("mainDialog", "name", None, QtGui.QApplication.UnicodeUTF8))
        self.tblPlayer.horizontalHeaderItem(1).setText(QtGui.QApplication.translate("mainDialog", "ip", None, QtGui.QApplication.UnicodeUTF8))
        self.tblPlayer.horizontalHeaderItem(2).setText(QtGui.QApplication.translate("mainDialog", "hwnd", None, QtGui.QApplication.UnicodeUTF8))
        self.tblScript.setSortingEnabled(True)
        self.tblScript.horizontalHeaderItem(0).setText(QtGui.QApplication.translate("mainDialog", "name", None, QtGui.QApplication.UnicodeUTF8))
        self.tblScript.horizontalHeaderItem(1).setText(QtGui.QApplication.translate("mainDialog", "desc", None, QtGui.QApplication.UnicodeUTF8))
        self.tblScript.horizontalHeaderItem(2).setText(QtGui.QApplication.translate("mainDialog", "shortcut key", None, QtGui.QApplication.UnicodeUTF8))
        self.btnExec.setText(QtGui.QApplication.translate("mainDialog", "执行", None, QtGui.QApplication.UnicodeUTF8))
        self.btnSaveScript.setText(QtGui.QApplication.translate("mainDialog", "保存", None, QtGui.QApplication.UnicodeUTF8))
        self.btnRefresh.setText(QtGui.QApplication.translate("mainDialog", "刷新", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QtGui.QApplication.translate("mainDialog", "脚本", None, QtGui.QApplication.UnicodeUTF8))
        self.btnAdd.setText(QtGui.QApplication.translate("mainDialog", "Add", None, QtGui.QApplication.UnicodeUTF8))
        self.btnDelete.setText(QtGui.QApplication.translate("mainDialog", "Delete", None, QtGui.QApplication.UnicodeUTF8))
        self.btnSave.setText(QtGui.QApplication.translate("mainDialog", "Save", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QtGui.QApplication.translate("mainDialog", "设置", None, QtGui.QApplication.UnicodeUTF8))

