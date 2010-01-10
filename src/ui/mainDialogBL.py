# -*- coding: utf-8 -*-
import sys
sys.path.append("..")
import helper
from dol import dolScript
from helper import WindowHelper

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