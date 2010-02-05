# -*- coding: utf-8 -*-
from dol import dolScript, dolSafeCall, dolCallEnum, enum, dolCall
import w32
import helper
from helper import WindowHelper, ProcessHelper
import time, datetime
import win32con, win32api
import pyqmacro
import dll
from PyQt4 import QtCore, QtGui
import threading
import ctypes
from dol import dolBuildShipScript

from dol.dolBuildShipData import *
from dll import Mouse, Key


ds = dolScript


from dol.global_ import *

window = None
#===============================================================================
# 前置脚本格式
# 
# def __xxx_pre(window):
#    //...
#    return (result, [arg1, arg2, ...])
#    
# #返回值第一个为bool 如果为false,则主脚本不会运行
# #返回值第二个为list 是主脚本第一和第二个参数之后的参数列表
#===============================================================================


    


def __dowhile(callable, args = [], interval = 0.2):
    while(not callable(*args)):
        time.sleep(interval)
        


def test(st,st2):
    print 'Test OK!!! String = %s / %s' % (st,st2)
    print window
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
    
    dolSafeCall.custom(proc, num)
    
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
    print 'disabled'
    return
    dolSafeCall.move(proc, dolCallEnum.MoveTo.Dock)

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
    dolSafeCall.move(proc, moveto)
    
def moveSea(hwnd, proc):
    '''
    出海
    '''
    
    dolSafeCall.moveSea(proc)

sailingLock = threading.Lock()

def __sailing_pre(window):
    hwndList = window.getPlayerHwndList()
    return (True, [hwndList])

def __findLead(hwnd):
    proc = WindowHelper.getProcByHwnd(hwnd)
    myid = dolScript.getPCID(proc)
    party = dolScript.getParty(proc)
    
    flag = False
    
    if(party != [] and myid == party[0]):
        flag = True
    
    win32api.CloseHandle(proc)
    return flag



def sailing(hwnd, proc, hwndList):
    '''
    航行异常处理
    '''
    global sailingLock
    
    myid = dolScript.getPCID(proc)
    party = dolScript.getParty(proc)
    
    leadHwnd = None
    
    stormWeather = 0x48
    myname = dolScript.getRoleName(proc)
    if(party != [] and myid != party[0]):
        for hwnd in hwndList:
            if(__findLead(hwnd)):
                leadHwnd = hwnd
        
        if(leadHwnd == None):
            print "找不到队长，退出"
            return
        
        
        log( "[%s] 开始队员异常处理" % (myname))
        count = 0
        while(True):
            #if(count % 20 == 0):
                #log( "[%s] 报到!" % (myname))
            
            if(dolScript.getLocationType(proc) != dolCallEnum.LocType.Sea):
                log( "[%s] Not in sea, exit" %(myname))
                break
        
            if(not dolScript.isOnline(proc)):
                log( "[%s] 断线了， 退出脚本" % (myname))
                beep(unicode("警告"), unicode("[%s] 断线了！！！" % (myname)))
                break
            
            if(dolScript.getWeather(proc) == stormWeather):
                log("遇到暴风")
                while(dolScript.getSailState(proc) != 0):
                    dolSafeCall.sail(proc, 0)
                    time.sleep(0.2)
                
                beep(unicode("警告"), unicode("遇到暴风!!!"))
                log('遇到暴风， 已停船， 停止脚本')
                break
            
            statetxt = dolScript.getShipState(proc)
            if(statetxt == "鼠患"):
                leadProc = WindowHelper.getProcByHwnd(leadHwnd)
                
                log("[%s]发现<%s>,请求队长发动驱除技能" % (myname, statetxt)) 
                __dowhile(dolScript.isNormal, [leadProc])
                dolSafeCall.custom(leadProc, 4)#f4 驱除
                time.sleep(2)
                win32api.CloseHandle(leadProc)
            count += 1
            time.sleep(0.5)
        log( "[%s] 退出脚本sailing" % (myname))
        return
    
    
    
    print "sailing()"
    sailingLock.acquire()
    print "Lock acquired"
    count = 0
    while(True):
        
        if(not dolScript.isOnline(proc)):
            log( "断线了， 退出脚本")
            beep(unicode("警告"), unicode("[%s] 断线了！！！" % (myname)))
            break
        
        if(dolScript.getLocationType(proc) != dolCallEnum.LocType.Sea):
            log( "Not in sea, exit")
            break
        
        
        
        #if(count % 10 == 0):
        #    log("Sailing() running...")
            
        if(dolScript.getCombat(proc) == 2): #被攻击
            log("停战")
            __dowhile(dolScript.isNormal, [proc])
            dolSafeCall.custom(proc, 6) #f6 要设置为停战
            time.sleep(0.3)
            
        
                    
        if(dolScript.getWeather(proc) == stormWeather):
            log("遇到暴风")
            while(dolScript.getSailState(proc) != 0):
                dolSafeCall.sail(proc, 0)
                time.sleep(0.2)
            
            beep(unicode("警告"), unicode("遇到暴风!!!"))
            log('遇到暴风， 已停船， 停止脚本')
            break
        
        
        while(dolScript.getHPRatio(proc) < 0.4):
            if(not dolScript.isOnline(proc)):
                break
                
            hp1 = dolScript.getHP(proc)
            log("要补行动力, 行动力 = %d" % (hp1))
            __dowhile(dolScript.isNormal, [proc])
            
            dolSafeCall.custom(proc, 7) #f7 要设置为料理
            time.sleep(2)
            hp2 = dolScript.getHP(proc)
            log("吃了一个料理, 行动力 = %d" % (hp2))
            if(hp1 == hp2):
                time.sleep(5)
            time.sleep(0.2)
        
        
            
        
        if(not dolScript.isAutoSail(proc) and dolScript.getSailState(proc) != 0 and dolScript.getWeather(proc) != stormWeather):
            log("操帆")
            __dowhile(dolScript.isNormal, [proc])
            dolSafeCall.custom(proc, 1) #f1 要设置为操帆
            time.sleep(2)
            
        statetxt = dolScript.getShipState(proc)
        if(statetxt == "鼠患" or statetxt == "海藻"):
            log("发现<%s>,发动驱除技能" % (statetxt)) 
            __dowhile(dolScript.isNormal, [proc])
            dolSafeCall.custom(proc, 4)#f4 驱除
            time.sleep(2) 
        
        
        sCount, sList = dolScript.getSkill(proc) 
        
        if(sCount != 3 and 75 not in sList): #75 == 警戒
            log("发动警戒技能") 
            __dowhile(dolScript.isNormal, [proc])
            dolSafeCall.custom(proc, 3)#f3 警戒
            time.sleep(2)
            
            
        if(sCount != 3 and 12 not in sList): #12 == 钓鱼
            log("发动钓鱼技能")
            __dowhile(dolScript.isNormal, [proc])
            dolSafeCall.custom(proc, 2) #f2 钓鱼
            time.sleep(2)
        
        preFatigue = dolScript.getFatigue(proc)
        if(preFatigue > 40):
            while(preFatigue > 40):
                if(not dolScript.isOnline(proc)):
                    break
                
                
                log("要消除疲劳, 疲劳 = %f" % (preFatigue))
                __dowhile(dolScript.isNormal, [proc])
                dolSafeCall.custom(proc, 7) #f7 要设置为料理
                fatigue = dolScript.getFatigue(proc)
                time.sleep(2)
                log("吃了一个料理, 疲劳 = %f" % (fatigue))
                
                if(fatigue == preFatigue):
                    log("料理并不能降低疲劳")
                    break
                else:
                    preFatigue = fatigue
        
            
        count += 1
        time.sleep(0.3)
    sailingLock.Release()
    print "Lock released"
    
def __BuildShip(hwnd, proc, onSea = None):
    if(onSea == None):
        onSea = False
    else:
        onSea = True
    print onSea
    city = blt()
    shipid = 0x19 #小飞
    woodid = 1
    storage = 180
    ticketnum = 2
    day = 6
    
    
    
    dolBuildShipScript.buildShip(hwnd, proc, city, shipid, woodid, storage, ticketnum, day, onSea)

def __feather(hwnd, proc):
    bossid = 0x1800349
    logger = TextLogger('FeatherLog.txt')
    myname = dolScript.getRoleName(proc)
    print myname
    def __alert():
        logger.log( "断线了，退出脚本")
        title = "警告"
        message = "[%s] 断线 !!!".decode('utf-8')
        message = message % (myname)
        message = message.encode('utf-8')
        beep(title, message)
    class Switcher():
        def __init__(self, switchList):
            self.switchList = switchList
            self.ptr = 0
        
        def getNext(self):
            self.ptr += 1
            if (self.ptr >= len(self.switchList)):
                self.ptr = self.ptr % len(self.switchList)
            return self.switchList[self.ptr]
    
    switch = Switcher([5, 6, 7, 8])
        
    while(True):
        if(not dolScript.isOnline(proc)):
            __alert()
            return
        while(dolCall.buy(proc, bossid, [-1, -1, (0xFFF, 68)])):
            logger.log('bought some ducks...')
            if(not dolScript.isOnline(proc)):
                __alert()
                return
            
            time.sleep(2)
            logger.log('use 1*')
            dolCall.custom(proc, 4) # f4放一星
            time.sleep(1)
        count = 0
        while(dolScript.getHPRatio(proc) < 0.7):
            if(not dolScript.isOnline(proc)):
                __alert()
                return
            logger.log('eat')
            dolCall.custom(proc, switch.getNext()) #f7 放料理
            time.sleep(1)
            count += 1
            if(count > dolScript.getHPMax(proc) / 20):
                logger.log('no food?')
                beep('Epic fail', 'No food !!!')
        
        logger.log('start to make feather')    
        dolCall.custom(proc, 3) #f3 放书
        time.sleep(2)
        Key("KeyClick", hwnd, 0x28) # down arrow
        time.sleep(1)
        Key("KeyClick", hwnd, 0xD) # enter
        time.sleep(3)
        
        Mouse("LClick", hwnd, 627, 495)
        time.sleep(1)
        
        hprecord = []
        waitSec = 5
        times = 6
        interval = waitSec / float(times)
        print interval
        for i in range(times):
            hprecord.append(-1)
        
        ptr = 0
        while(True):
            if(not dolScript.isOnline(proc)):
                __alert()
                return
            hp = dolScript.getHP(proc)
            if(hp < 100):
                logger.log('hp low during making')
                dolCall.custom(proc, 7)
                for i in range(times):
                    hprecord[i] = -1
                time.sleep(1)
            
            hprecord[ptr] = hp
            beforeptr = ptr
            ptr += 1
            ptr = ptr % times
            print hprecord
            if(hprecord[beforeptr] == hprecord[ptr]):
                if(hprecord[beforeptr] < 10):
                    logger.log('no food?')
                    beep('Epic fail', 'No food !!!')
                
                logger.log('no materials')
                time.sleep(2)
                break    
            time.sleep(interval)
           
        while(dolCall.sell(proc, bossid, [(0x186b2f, 30)])): #0x186b2f == 羽毛的id
            if(not dolScript.isOnline(proc)):
                __alert()
                return
            logger.log('selling feathers')
            time.sleep(2)
        time.sleep(2)
    
    
    
    
    
    