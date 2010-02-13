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


class readMap(rtBaseClass):
    def __init__(self, proc, cityRead, citySec, serHwnd):
        rtBaseClass.__init__(self)
        self.cityRead = cityRead
        self.citySec = citySec
        self.cityList = [cityRead, citySec]
        self.nextDoFunc = None
        self.nextDoPara = None
        self.proc = proc
        self.serHwnd = serHwnd
        
        hlper = helper.ProcessHelper()
        self.hwnd = hlper.getHwndByProc(proc)
    
    
    def read(self):
        self.nextDoFunc = self.lib2Dock
        
        self.nextDoPara = []
        
        
        proc = self.proc
        while(True):
            dolCall.openDialog(proc, self.cityRead.manID, 0x83)
            dountil(dolScript.isDialogOpen, [proc])
            
            while(dolScript.getToRead(proc) != 5): #5是美术
                dll.Key('KeyClick', self.hwnd, win32con.VK_LEFT)
                time.sleep(1)
            
            while(dolScript.getInt(proc, dolCall.CALLADDR.DIALOG) != 0 and not dolScript.isReading(proc)):
                
                dll.Mouse('LClick', self.hwnd, 547, 240)
                time.sleep(1)
                
            #547, 240
            
            while(True):
                if(dolScript.inLog(proc, '頭腦疲勞', 3)):
                    log('疲勞了...')
                    return
                if(dolScript.inLog(proc, '得到了教會宗教畫的地圖', 3)):
                    log('讀到圖')
                    bossid = dolScript.getPCID(proc)
                    dolCall.openDialog(proc, bossid, 0x20)
                    myname = dolScript.getRoleName(proc)
                    dountil(dolScript.isDialogOpen, [proc])
                    win32gui.SetActiveWindow(self.hwnd)
                    msgBox(myname, '读到图。请摆露天')
                    time.sleep(1)
                    
                    tarhwnd = self.serHwnd
                    tarproc = helper.WindowHelper.getProcByHwnd(tarhwnd)
                    self.makeBuy(tarhwnd, tarproc)
                    win32api.CloseHandle(tarproc)
                    break
                    
                time.sleep(0.2)
        
        
    
    def makeBuy(self, tarhwnd, tarproc):
        lockAddr = 0xAFD600
        proc = self.proc
        myid = dolScript.getPCID(proc)
        tarname = dolScript.getRoleName(tarproc)
        print tarname
        while(True):
            
            while(dolScript.getInt(tarproc, lockAddr) != 0):
                print dolScript.getInt(tarproc, lockAddr)
                time.sleep(0.2)
            
            try:
                dolCall.writeMem(tarproc, lockAddr, dolCall.c_uint(myid))
            except dolCall.MemException, e:
                pass
                
            if(dolCall.getInt(tarproc, lockAddr) == myid):
                break
        
        dolCall.openDialog(tarproc, myid, 0x32)
        dountil(dolScript.isDialogOpen, [tarproc])
        win32gui.SetActiveWindow(tarhwnd)
        msgBox(tarname, '請購買露天。。。')

        time.sleep(2)
        dolCall.writeMem(tarproc, lockAddr, dolCall.c_uint(0))
        
    
    def toReadDock(self):
        proc = self.proc
        cityID = self.cityRead.cityID
        gotoCity(proc, cityID, self.citySec.cityRouteDict[cityID])
        self.nextDoFunc = self.dock2Lib
        self.nextDoPara = []    
    
    def toSecDock(self):    
        proc = self.proc
        cityID = self.citySec.cityID
        
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
        proc = self.proc
        while(dolScript.getLocationType(proc) != dolCallEnum.LocType.City):
            dolCall.move(proc, self.cityRead.downShip)
            time.sleep(1.5)
        x, y = self.cityRead.libEnterPos
        dolCall.walk(proc, x, y)
        time.sleep(1)
        dolCall.enterDoor(proc, self.cityRead.libEnterID)
        x, y = self.cityRead.toReadPos
        dolCall.walk(proc, x, y)
        
        self.nextDoFunc = self.read
        self.nextDoPara = []
        
        
        
        
    
    def start(self):
        proc = self.proc
        locName = dolScript.getLocation(proc)
        if(locName == self.citySec.dockName):
            print 'In citySec dock'
            self.nextDoFunc = self.toReadDock
            self.nextDoPara = []
            
        elif(locName == self.cityRead.dockName):
            print 'In cityRead dock'
            self.nextDoFunc = self.dock2Lib
            self.nextDoPara = []
            
        elif(locName == self.cityRead.libName):
            print 'In library'
            self.nextDoFunc = self.read
            self.nextDoPara = []
        else:
            print "Help!! I don't know how to start !!! "

    
    def main(self):
        self.start()
        
        while(True):
            self.nextDoFunc(*self.nextDoPara)
            print 'wait for next do'
            time.sleep(2)
            
def rmmain(proc):
    
    serHwnd = 0x715ce
    #tarproc = helper.WindowHelper.getProcByHwnd(serHwnd)
    cRead = readMapDta.sw()
    cSec = readMapDta.fl()
    rm = readMap(proc, cRead, cSec, serHwnd)
    
    rm.main()
    #win32api.CloseHandle(tarproc)