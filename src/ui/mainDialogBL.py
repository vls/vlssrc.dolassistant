# -*- coding: utf-8 -*-
import sys
sys.path.append("..")
import helper
from dol import dolScript
from helper import WindowHelper
import win32api, win32gui, win32con

def getDolList():
    '''获取机器内所有大航海OL的信息
    return (name, hwnd, id)
    '''
    nameList = []
    winHelper = helper.WindowHelper()
    hwndList = dolScript.getDolHwndList()
    for hwnd in hwndList:
        proc = WindowHelper.getProcByHwnd(hwnd)
        name = dolScript.getRoleName(proc)
        id = dolScript.getPCID(proc)
        nameList.append((name, hwnd, id))
    
    return nameList

def scriptWrap(callable, hwnd, xargs = None):
    '''
    运行脚本封装函数
    '''
    if(xargs == None):
        xargs = []
    
    
    proc = WindowHelper.getProcByHwnd(hwnd)
    
    xargs.insert(0, proc)
    xargs.insert(0, hwnd)
    callable(*xargs)
    
    win32api.CloseHandle(proc)

def wiseMin(hwndList):
    for hwnd in hwndList:
        proc = WindowHelper.getProcByHwnd(hwnd)
        myid = dolScript.getPCID(proc)
        party = dolScript.getParty(proc)
        if(not (len(party) != 0 and myid == party[0])):
            win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)
        
        win32api.CloseHandle(proc)
            
            