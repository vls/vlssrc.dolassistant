# -*- coding: utf-8 -*-
from dol import dolScript, dolSafeCall, dolCallEnum, enum
import w32
import helper
from helper import WindowHelper, ProcessHelper
import time, datetime
import win32con, win32api
import pyqmacro
import dll
from PyQt4 import QtCore, QtGui
import threading

ds = dolScript

def __beep(title = "", message = ""):
    win32api.MessageBeep(win32con.MB_ICONEXCLAMATION)
    win32api.MessageBox(None, unicode(title), unicode(message), win32con.MB_ICONERROR)
    
def __dowhile(callable, args = [], interval = 0.2):
    while(not callable(*args)):
        time.sleep(interval)
        
def __log(msg):
    print "%s : %s " % (datetime.datetime.now(), msg)

def test(st,st2):
    print 'Test OK!!! String = %s / %s' % (st,st2)
    return None

def test2():
    '''注释
    '''
    print 'Test2 OK!!!'

def __getInt(title = "", label = "", default = 1):
    result, dialog = __prompt(QtGui.QInputDialog.IntInput, default, title, label)
    return (result, dialog.intValue())

def __prompt(inputmode, default, title = "", label = ""):
    
    dialog = QtGui.QInputDialog()
    dialog.setInputMode(inputmode)
    
    if(inputmode == dialog.IntInput):
        dialog.setIntValue(default)
    elif(inputmode == dialog.DoubleInput):
        dialog.setDoubleValue(default)
    elif(inputmode == dialog.TextInput):
        dialog.setTextValue(default)
    
    dialog.setWindowTitle(title)
    dialog.setLabelText(label)
    dialog.setModal(True)
    dialog.activateWindow()
    result = dialog.exec_()
    return (result, dialog)

def __custom_pre(window):
    #value, flag = QtGui.QInputDialog.getInt(None, unicode("使用自订栏"), "1 <= x <= 8")
    
    result, value = __getInt(unicode('使用自订栏'), "1 <= x <= 8")
    
    return (result, [value])   
    #return (False, 123)

def custom(hwnd, proc, num):
    '''
    使用自订栏
    '''
    print 'custom'
    
    dolSafeCall.custom_safe(proc, num)
    
def testHwnd(hwnd):
    '''测试'''
    print hwnd
    
def follow(hwnd, proc):
    '''跟随TD
    '''
    
    party = ds.getParty(proc)
    
    if(len(party) == 0):
        print "%d 无组队！" % (hwnd)
        return
    
    myid = ds.getPCID(proc)
    if(myid == party[0]):
        print "[%d] 我是队长" % (hwnd)
        return
    
    dolSafeCall.follow_safe(proc, party[0])
    print 'follow end'
    
    
def toDock(hwnd, proc):
    '''
    进入码头
    '''
    
    userid = dolScript.getPCID(proc)
    
    dolSafeCall.move(proc, userid, dolCallEnum.MoveTo.Dock)

def __enterCity_pre(window):
    result, value = __getInt(unicode('从哪里进入城市'), unicode('1=码头广场, 2=广场, 3=商业地区, 4=商务会馆'))
    retValue = None
    if(value == 1):
        retValue = dolCallEnum.MoveTo.DockPlaza
    elif(value == 2):
        retValue = dolCallEnum.MoveTo.Plaza
    elif(value == 3):
        retValue = dolCallEnum.MoveTo.Biz
    elif(value == 4):
        retValue = dolCallEnum.MoveTo.BizHouse
    
    return (result, [retValue])

def enterCity(hwnd, proc, moveto):
    '''
    进入城市
    '''
    userid = dolScript.getPCID(proc)
    dolSafeCall.move(proc, userid, moveto)
    
def moveSea(hwnd, proc):
    '''
    出海
    '''
    userid = dolScript.getPCID(proc)
    dolSafeCall.moveSea(proc, userid)

sailingLock = threading.Lock()

def sailing(hwnd, proc):
    '''
    航行异常处理
    '''
    global sailingLock
    print "sailing()"
    sailingLock.acquire()
    print "Lock acquired"
    count = 0
    while(True):
        if(dolScript.getLocationType(proc) != dolCallEnum.LocType.Sea):
            print "Not in sea, exit"
            break
        
        
        if(count % 10 == 0):
            __log("Sailing() running...")
            
        if(dolScript.getCombat(proc) == 2): #被攻击
            __log("停战")
            __dowhile(dolScript.isNormal, [proc])
            dolSafeCall.custom_safe(proc, 5) #f5 要设置为停战
            
        
                    
        if(dolScript.getWeather(proc) == 64):
            dolSafeCall.sail(proc, 0)
            __log("遇到暴风")
            __beep(unicode("警告"), unicode("遇到暴风!!!"))
        
        
        while(dolScript.getHPRatio(proc) < 0.4):
            hp1 = dolScript.getHP(proc)
            __log("要补行动力, 行动力 = %d" % (hp1))
            __dowhile(dolScript.isNormal, [proc])
            
            dolSafeCall.custom_safe(proc, 8) #f8 要设置为料理
            time.sleep(2)
            hp2 = dolScript.getHP(proc)
            __log("吃了一个料理, 行动力 = %d" % (hp2))
            if(hp1 == hp2):
                time.sleep(3)
            time.sleep(0.2)
        
        
            
        
        if(not dolScript.isAutoSail(proc)):
            __log("操帆")
            __dowhile(dolScript.isNormal, [proc])
            dolSafeCall.custom_safe(proc, 1) #f1 要设置为操帆
            time.sleep(2)
            
        statetxt = dolScript.getShipState(proc)
        if(statetxt == "鼠患" or statetxt == "海藻"):
            __log("发现<%s>,发动驱除技能" % (statetxt)) 
            __dowhile(dolScript.isNormal, [proc])
            dolSafeCall.custom_safe(proc, 4)#f4 驱除
            time.sleep(2) 
        
        
        sCount, sList = dolScript.getSkill(proc) 
        
        if(sCount != 3 and 75 not in sList): #75 == 警戒
            __log("发动警戒技能") 
            __dowhile(dolScript.isNormal, [proc])
            dolSafeCall.custom_safe(proc, 3)#f3 警戒
            time.sleep(2)
            
            
        if(sCount != 3 and 12 not in sList): #12 == 钓鱼
            __log("发动钓鱼技能")
            __dowhile(dolScript.isNormal, [proc])
            dolSafeCall.custom_safe(proc, 2) #f2 钓鱼
            time.sleep(2)
        
        preFatigue = dolScript.getFatigue(proc)
        if(preFatigue > 40):
            while(preFatigue > 40):
                __log("要消除疲劳, 疲劳 = %f" % (preFatigue))
                __dowhile(dolScript.isNormal, [proc])
                dolSafeCall.custom_safe(proc, 8) #f8 要设置为料理
                fatigue = dolScript.getFatigue(proc)
                time.sleep(2)
                __log("吃了一个料理, 疲劳 = %f" % (fatigue))
                
                if(fatigue == preFatigue):
                    __log("料理并不能降低疲劳")
                    break
                else:
                    preFatigue = fatigue
        
            
        count += 1
        time.sleep(0.3)
    sailingLock.Release()
    print "Lock released"