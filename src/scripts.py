# -*- coding: utf-8 -*-
from dol import dolScript
import w32
import helper
from helper import WindowHelper, ProcessHelper
import time
import win32con
import pyqmacro
import dll

ds = dolScript

def __dowhile(func, args, interval = 0.1):
    while(func(*args)):
        time.sleep(interval)

def test(st,st2):
    print 'Test OK!!! String = %s / %s' % (st,st2)
    return None

def test2():
    '''注释
    '''
    print 'Test2 OK!!!'
    
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
    __dowhile(lambda p: not ds.isNormal(p), [proc])
    
    tabid = ds.getTabId(proc)
    while(tabid == 0 or tabid != party[0]):
        print "[%s]: 找啊找,要找%d, 找到%d" % (name, party[0], tabid)
        dll.Key("KeyClick", hwnd, 9)# TAB
        time.sleep(0.01)
        tabid = ds.getTabId(proc)
        print tabid
    