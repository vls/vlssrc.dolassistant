# -*- coding: utf-8 -*-
from dol import dolScript, dolSafeCall
import w32
import helper
from helper import WindowHelper, ProcessHelper
import time
import win32con, win32api
import pyqmacro
import dll
from PyQt4 import QtCore, QtGui

ds = dolScript


def __dowhile(callable, args = [], interval = 0.2):
    while(not callable(*args)):
        time.sleep(interval)

def test(st,st2):
    print 'Test OK!!! String = %s / %s' % (st,st2)
    return None

def test2():
    '''注释
    '''
    print 'Test2 OK!!!'

def __custom_pre(window):
    #value, flag = QtGui.QInputDialog.getInt(None, unicode("使用自订栏"), "1 <= x <= 8")
    
    dialog = QtGui.QInputDialog()
    dialog.setInputMode(QtGui.QInputDialog.IntInput)
    dialog.setLabelText("1 <= x <= 8")
    dialog.setModal(True)
    
    #dialog.show()
    #dialog.raise_()
    #print dialog.intValue
    dialog.activateWindow()
    
    dialog.setIntValue(1)
    result = dialog.exec_()
    print result
    return (result, [dialog.intValue()])
    
    #return (flag, [value])   
    #return (False, 123)

def custom(hwnd, num):
    '''
    使用自订栏
    '''
    print 'custom'
    proc = WindowHelper.getProcByHwnd(hwnd)
    
    dolSafeCall.custom_safe(proc, num)
    
    win32api.CloseHandle(proc)
    
def testHwnd(hwnd):
    '''测试'''
    print hwnd
    
def follow(hwnd):
    '''跟随TD
    '''
    proc = WindowHelper.getProcByHwnd(hwnd)
    
    party = ds.getParty(proc)
    
    if(len(party) == 0):
        print "%d 无组队！" % (hwnd)
        return
    
    myid = ds.getPCID(proc)
    if(myid == party[0]):
        print "我是队长"
        return
    name = ds.getRoleName(proc)
    __dowhile(ds.isNormal, [proc])
    
    dolSafeCall.follow(proc, party[0])
    
    win32api.CloseHandle(proc)
    