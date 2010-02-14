# -*- coding: utf-8 -*-
import sys
sys.path.append('..')
from rtBase import rtBaseClass, rtCityBase
from global_ import log, dowhile, dountil, beep, msgBox
from roundTrip import gotoCity
import dolScript
import dolCall
import dolCallEnum
import time
import readMapDta
import win32con, win32gui, win32api
import dll
import helper

from threadpool import ThreadPool, WorkRequest

from global_ import MutexGuard

import threading

mutex = threading.Lock()


class readMapClass(rtBaseClass):
    def __init__(self, proc, cityRead, citySec, serHwnd, readMsg, fellowList = None):
        rtBaseClass.__init__(self)
        self.cityRead = cityRead
        self.citySec = citySec
        self.cityList = [cityRead, citySec]
        self.nextDoFunc = None
        self.nextDoPara = None
        self.proc = proc
        self.serHwnd = serHwnd
        self.readMsg = readMsg
        self.fellowList = []
        if(fellowList != None):
            self.fellowList = fellowList
        
        self.pool = ThreadPool(len(self.fellowList))
        
        hlper = helper.ProcessHelper()
        self.hwnd = hlper.getHwndByProc(proc)
    
    def makeAllDo(self, callfunc, paraList = None, hwndPos = -1, procPos = 0):
        if(paraList == None):
            paraList = []
        for hwnd in self.fellowList:
            req = WorkRequest(self.funcWrap, [hwnd, callfunc, list(paraList), procPos, hwndPos])
            self.pool.putRequest(req)
            
    
    def funcWrap(self, hwnd, callfunc, paraList, procPos, hwndPos):
        
        procGuard = helper.ProcGuard(hwnd)
        print 'paraList before = %s' % (paraList)
        if(hwndPos != -1):
            paraList.insert(hwndPos, hwnd)
        
        if(procPos != -1):
            paraList.insert(procPos, procGuard.proc)
            
        print 'paraList = %s' % (paraList)
        callfunc(*paraList)
    
    def read(self, hwnd, proc, isFellow = False):
        print 'read'
        myname = dolScript.getRoleName(proc)
        print '[%s](%d) start to read. (isFellow = %s)' % (myname, hwnd, isFellow)
        statusAddr = 0xAFD700
        
        def __markOK(_hwnd):
            procGuard = helper.ProcGuard(_hwnd)
            dolCall.writeMem(procGuard.proc, statusAddr, dolCall.c_uint(0))
        
        x, y = self.cityRead.toReadPos
        if(dolScript.getLandFollow(proc) == 0):
            dolCall.walk(proc, x, y)
        
        if(not isFellow):
            for _hwnd in self.fellowList:
                __markOK(_hwnd)
            self.makeAllDo(self.read, [True], hwndPos = 0, procPos = 1)
            self.nextDoFunc = self.lib2Dock
            
            self.nextDoPara = []
        
        
        
        
        while(True):
            while(not dolScript.isDialogOpen(proc)):
                dolCall.openDialog(proc, self.cityRead.manID, 0x83)
                time.sleep(0.5)
            dountil(dolScript.isDialogOpen, [proc])
            
            while(dolScript.getToRead(proc) != 5): #5是美术
                print '[%s](%d) press left arrow' % (myname, hwnd)
                dll.Key('KeyClick', hwnd, win32con.VK_LEFT)
                time.sleep(1)
            
            print 'Click begin'
            print "-------%s %s-------" % (dolScript.getInt(proc, dolCall.CALLADDR.DIALOG) != 0, not dolScript.isReading(proc))
            while(dolScript.getInt(proc, dolCall.CALLADDR.DIALOG) != 0 and not dolScript.isReading(proc)):
                print "%s %s" % (dolScript.getInt(proc, dolCall.CALLADDR.DIALOG) != 0, not dolScript.isReading(proc))
                
                dll.Mouse('LClick', hwnd, 547, 240)
                time.sleep(2)
            print 'Click end'
                
            #547, 240
            
            while(True):
                print 'reading... (Money = %d)' % (dolScript.getMoney(proc))
                if(dolScript.inLog(proc, '頭腦疲勞', 3)):
                    log('疲勞了...')
                    startTime = time.time()
                    if(isFellow):
                        procGuard = helper.ProcGuard(hwnd)
                        print '[%s] 疲劳了， 写内存' % (myname)
                        dolCall.writeMem(procGuard.proc, statusAddr, dolCall.c_uint(1))
                    else:
                        okFellowDict = {}
                        if(len(self.fellowList) > 0):
                            while(True):
                                if(len(okFellowDict) == len(self.fellowList) or time.time() - startTime > 120):
                                    #timeout一分钟也走人
                                    log('全部疲倦了，走人')
                                    return
                                
                                for _hwnd in self.fellowList:
                                    if(okFellowDict.has_key(_hwnd)):
                                        continue
                                    procGuard = helper.ProcGuard(_hwnd)
                                    if(not dolScript.isOnline(procGuard.proc)):
                                        okFellowDict[_hwnd] = -1
                                    
                                    
                                    if(dolScript.getInt(procGuard.proc, statusAddr) != 0):
                                        okFellowDict[_hwnd] = 1
                                time.sleep(0.5) 
                    
                    return
                
                
                if(dolScript.inLog(proc, self.readMsg, 3)):
                    log('讀到圖')
                    bossid = dolScript.getPCID(proc)
                    dolCall.openDialog(proc, bossid, 0x20)
                    myname = dolScript.getRoleName(proc)
                    dountil(dolScript.isDialogOpen, [proc])
                    msgBox(myname, '读到图。准备弹出窗口……')
                    
                    win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
                    win32gui.SetActiveWindow(hwnd)
                    
                    win32gui.SetForegroundWindow(hwnd)
                    msgBox(myname, '请在摆好露天后点击确定。（将会有购买窗口弹出……）')
                    dowhile(dolScript.isDialogOpen, [proc])
                    win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)
                    time.sleep(1)
                    
                    tarhwnd = self.serHwnd
                    
                    self.makeBuy(tarhwnd, hwnd)
                    break
                    
                time.sleep(0.2)
        
        
    
    def makeBuy(self, tarhwnd, myhwnd):
        tarprocGuard = helper.ProcGuard(tarhwnd)
        myprocGuard = helper.ProcGuard(myhwnd)
        
        proc = myprocGuard.proc
        tarproc = tarprocGuard.proc
        
        myid = dolScript.getPCID(proc)
        myname = dolScript.getRoleName(proc)
        tarname = dolScript.getRoleName(tarproc)
        print tarname
        
        lock = MutexGuard(mutex)
        
        dolCall.openDialog(tarproc, myid, 0x32)
        dountil(dolScript.isDialogOpen, [tarproc])
        
        win32gui.ShowWindow(tarhwnd, win32con.SW_RESTORE)
        win32gui.SetActiveWindow(tarhwnd)
        win32gui.SetForegroundWindow(tarhwnd)
        msgBox(tarname, '請購買 [' + myname + '] 的露天……')
        win32gui.ShowWindow(tarhwnd, win32con.SW_MINIMIZE)
        time.sleep(2)
        
    
    def toReadDock(self):
        proc = self.proc
        cityID = self.cityRead.cityID
        
        self.makeAllDo(dolCall.moveSea)
            
        while(dolScript.getLocationType(proc) == dolCallEnum.LocType.Dock):
            dolCall.moveSea(proc)
            time.sleep(0.5)
        
        myid = dolScript.getPCID(proc)
        self.makeAllDo(dolCall.follow, [myid])
        
        gotoCity(proc, cityID, self.citySec.cityRouteDict[cityID])
        self.nextDoFunc = self.dock2Lib
        self.nextDoPara = []    
    
    def toSecDock(self):    
        proc = self.proc
        cityID = self.citySec.cityID
        
        self.makeAllDo(dolCall.moveSea)
            
        while(dolScript.getLocationType(proc) == dolCallEnum.LocType.Dock):
            dolCall.moveSea(proc)
            time.sleep(0.5)
        
        myid = dolScript.getPCID(proc)
        self.makeAllDo(dolCall.follow, [myid])
            
        gotoCity(proc, cityID, self.cityRead.cityRouteDict[cityID])
        self.nextDoFunc = self.toReadDock
        self.nextDoPara = []

    def lib2Dock(self):
        proc = self.proc
        while(dolScript.getLocationType(proc) == dolCallEnum.LocType.House):
            dolCall.enterDoor(proc, self.cityRead.libOutID)
            time.sleep(0.5)
        while(dolScript.getLocationType(proc) == dolCallEnum.LocType.City):
            dolCall.move(proc, dolCallEnum.MoveTo.Dock)
            time.sleep(0.5)
        
        self.nextDoFunc = self.toSecDock
        self.nextDoPara = []
    
    def dock2Lib(self):
        self.makeAllDo(dolCall.move, [self.cityRead.downShip])
        
        proc = self.proc
        while(dolScript.getLocationType(proc) != dolCallEnum.LocType.City):
            dolCall.move(proc, self.cityRead.downShip)
            time.sleep(1.5)
        
        myid = dolScript.getPCID(proc)
        self.makeAllDo(dolCall.follow, [myid])    
        
        x, y = self.cityRead.libEnterPos
        dolCall.walk(proc, x, y)
        time.sleep(1)
        dolCall.enterDoor(proc, self.cityRead.libEnterID)
        
        self.nextDoFunc = self.read
        self.nextDoPara = [self.hwnd, self.proc]
        
        
        
        
    
    def start(self):
        proc = self.proc
        locName = dolScript.getLocation(proc)
        if(locName == self.citySec.getDockName()):
            print 'In citySec dock'
            self.nextDoFunc = self.toReadDock
            self.nextDoPara = []
            
        elif(locName == self.cityRead.getDockName() or locName == self.cityRead.name):
            print 'In cityRead dock'
            self.nextDoFunc = self.dock2Lib
            self.nextDoPara = []
            
        elif(locName == self.cityRead.libName):
            print 'In library'
            self.nextDoFunc = self.read
            self.nextDoPara = [self.hwnd, self.proc]
        
        else:
            print "Help!! I don't know how to start !!! "

    
    def main(self):
        print 'readMap main()'
        self.start()
        
        while(True):
            self.nextDoFunc(*self.nextDoPara)
            print 'wait for next do'
            time.sleep(2)
            
def rmmain(proc):
    
    serHwnd = 0xe09ca
    #tarproc = helper.WindowHelper.getProcByHwnd(serHwnd)
    cRead = readMapDta.london()
    cSec = readMapDta.duofo()
    print cSec.cityID
    
    rm = readMapClass(proc, cRead, cSec, serHwnd, '得到了教會祭器的地圖')
    
    rm.main()