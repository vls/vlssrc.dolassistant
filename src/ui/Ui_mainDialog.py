# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainDialog.ui'
#
# Created: Sat Jan 23 22:19:17 2010
#      by: PyQt4 UI code generator 4.6.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_mainDialog(object):
    def setupUi(self, mainDialog):
        mainDialog.setObjectName("mainDialog")
        mainDialog.resize(419, 450)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(mainDialog.sizePolicy().hasHeightForWidth())
        mainDialog.setSizePolicy(sizePolicy)
        mainDialog.setAutoFillBackground(False)
        self.tabWidget = QtGui.QTabWidget(mainDialog)
        self.tabWidget.setGeometry(QtCore.QRect(10, 10, 401, 431))
        self.tabWidget.setObjectName("tabWidget")
        self.tab_4 = QtGui.QWidget()
        self.tab_4.setObjectName("tab_4")
        self.txt = QtGui.QPlainTextEdit(self.tab_4)
        self.txt.setGeometry(QtCore.QRect(0, 0, 391, 401))
        self.txt.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.txt.setUndoRedoEnabled(False)
        self.txt.setReadOnly(True)
        self.txt.setObjectName("txt")
        self.tabWidget.addTab(self.tab_4, "")
        self.tab = QtGui.QWidget()
        self.tab.setObjectName("tab")
        self.tblScript = QtGui.QTableWidget(self.tab)
        self.tblScript.setGeometry(QtCore.QRect(10, 210, 369, 141))
        self.tblScript.setEditTriggers(QtGui.QAbstractItemView.DoubleClicked|QtGui.QAbstractItemView.EditKeyPressed)
        self.tblScript.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.tblScript.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
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
        self.btnSaveScript.setGeometry(QtCore.QRect(110, 360, 80, 25))
        self.btnSaveScript.setObjectName("btnSaveScript")
        self.btnRefresh = QtGui.QPushButton(self.tab)
        self.btnRefresh.setGeometry(QtCore.QRect(10, 180, 80, 25))
        self.btnRefresh.setObjectName("btnRefresh")
        self.progLoad = QtGui.QProgressBar(self.tab)
        self.progLoad.setGeometry(QtCore.QRect(240, 180, 118, 23))
        self.progLoad.setProperty("value", 0)
        self.progLoad.setObjectName("progLoad")
        self.tblPlayer = QtGui.QTableWidget(self.tab)
        self.tblPlayer.setGeometry(QtCore.QRect(10, 10, 361, 161))
        self.tblPlayer.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.tblPlayer.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tblPlayer.setObjectName("tblPlayer")
        self.tblPlayer.setColumnCount(3)
        self.tblPlayer.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.tblPlayer.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tblPlayer.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.tblPlayer.setHorizontalHeaderItem(2, item)
        self.btnRefreshScript = QtGui.QPushButton(self.tab)
        self.btnRefreshScript.setGeometry(QtCore.QRect(10, 360, 80, 25))
        self.btnRefreshScript.setObjectName("btnRefreshScript")
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
        self.tab_3 = QtGui.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.tblNetPlayer = QtGui.QTableWidget(self.tab_3)
        self.tblNetPlayer.setGeometry(QtCore.QRect(10, 20, 369, 165))
        self.tblNetPlayer.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.tblNetPlayer.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tblNetPlayer.setShowGrid(True)
        self.tblNetPlayer.setGridStyle(QtCore.Qt.SolidLine)
        self.tblNetPlayer.setObjectName("tblNetPlayer")
        self.tblNetPlayer.setColumnCount(3)
        self.tblNetPlayer.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.tblNetPlayer.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tblNetPlayer.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.tblNetPlayer.setHorizontalHeaderItem(2, item)
        self.tabWidget.addTab(self.tab_3, "")

        self.retranslateUi(mainDialog)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QObject.connect(self.btnAdd, QtCore.SIGNAL("clicked()"), mainDialog.addItem)
        QtCore.QObject.connect(self.btnDelete, QtCore.SIGNAL("clicked()"), mainDialog.deleteItem)
        QtCore.QObject.connect(self.btnSave, QtCore.SIGNAL("clicked()"), mainDialog.saveItems)
        QtCore.QObject.connect(self.btnRefresh, QtCore.SIGNAL("clicked()"), mainDialog.setPlayerList)
        QtCore.QObject.connect(self.btnExec, QtCore.SIGNAL("clicked()"), mainDialog.execScript)
        QtCore.QObject.connect(self.btnRefreshScript, QtCore.SIGNAL("clicked()"), mainDialog.refreshScript)
        QtCore.QObject.connect(self.btnSaveScript, QtCore.SIGNAL("clicked()"), mainDialog.saveScript)
        QtCore.QMetaObject.connectSlotsByName(mainDialog)

    def retranslateUi(self, mainDialog):
        mainDialog.setWindowTitle(QtGui.QApplication.translate("mainDialog", "控制端", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), QtGui.QApplication.translate("mainDialog", "信息", None, QtGui.QApplication.UnicodeUTF8))
        self.tblScript.setSortingEnabled(True)
        self.tblScript.horizontalHeaderItem(0).setText(QtGui.QApplication.translate("mainDialog", "name", None, QtGui.QApplication.UnicodeUTF8))
        self.tblScript.horizontalHeaderItem(1).setText(QtGui.QApplication.translate("mainDialog", "desc", None, QtGui.QApplication.UnicodeUTF8))
        self.tblScript.horizontalHeaderItem(2).setText(QtGui.QApplication.translate("mainDialog", "shortcut key", None, QtGui.QApplication.UnicodeUTF8))
        self.btnExec.setText(QtGui.QApplication.translate("mainDialog", "执行", None, QtGui.QApplication.UnicodeUTF8))
        self.btnSaveScript.setText(QtGui.QApplication.translate("mainDialog", "保存", None, QtGui.QApplication.UnicodeUTF8))
        self.btnRefresh.setText(QtGui.QApplication.translate("mainDialog", "刷新", None, QtGui.QApplication.UnicodeUTF8))
        self.tblPlayer.horizontalHeaderItem(0).setText(QtGui.QApplication.translate("mainDialog", "name", None, QtGui.QApplication.UnicodeUTF8))
        self.tblPlayer.horizontalHeaderItem(1).setText(QtGui.QApplication.translate("mainDialog", "hwnd", None, QtGui.QApplication.UnicodeUTF8))
        self.tblPlayer.horizontalHeaderItem(2).setText(QtGui.QApplication.translate("mainDialog", "id", None, QtGui.QApplication.UnicodeUTF8))
        self.btnRefreshScript.setText(QtGui.QApplication.translate("mainDialog", "刷新", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QtGui.QApplication.translate("mainDialog", "脚本", None, QtGui.QApplication.UnicodeUTF8))
        self.btnAdd.setText(QtGui.QApplication.translate("mainDialog", "Add", None, QtGui.QApplication.UnicodeUTF8))
        self.btnDelete.setText(QtGui.QApplication.translate("mainDialog", "Delete", None, QtGui.QApplication.UnicodeUTF8))
        self.btnSave.setText(QtGui.QApplication.translate("mainDialog", "Save", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QtGui.QApplication.translate("mainDialog", "设置", None, QtGui.QApplication.UnicodeUTF8))
        self.tblNetPlayer.setSortingEnabled(True)
        self.tblNetPlayer.horizontalHeaderItem(0).setText(QtGui.QApplication.translate("mainDialog", "name", None, QtGui.QApplication.UnicodeUTF8))
        self.tblNetPlayer.horizontalHeaderItem(1).setText(QtGui.QApplication.translate("mainDialog", "ip", None, QtGui.QApplication.UnicodeUTF8))
        self.tblNetPlayer.horizontalHeaderItem(2).setText(QtGui.QApplication.translate("mainDialog", "hwnd", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QtGui.QApplication.translate("mainDialog", "Page", None, QtGui.QApplication.UnicodeUTF8))

