# -*- coding: utf-8 -*-
import sys
sys.path.append('..')
import dll
import time
import dolCall, dolScript, dolCallEnum
from global_ import *


def buildShip(hwnd, proc, city, shipid, woodid, storage, ticketnum, day, onSea):
    bossid = city.bossid
    bossx, bossy = city.bosspos
    cityid = city.cityid
    userid = dolScript.getPCID(proc)
    
    while(True): 
        
        if(not onSea):
            dolCall.walk(proc, bossx, bossy)
            log("start to buildship")
            dolCall.buildShip(proc, shipid, woodid, storage, bossid)
            time.sleep(2)
            
            while(dolScript.getLocationType(proc) != dolCallEnum.LocType.Dock):
                log("move to dock")
                dolCall.move(proc, dolCallEnum.MoveTo.Dock)
                time.sleep(1.5)
                
            while(dolScript.getLocationType(proc) != dolCallEnum.LocType.Sea):
                log("moveSea")
                dolCall.moveSea(proc)
                time.sleep(1.5)
            
        if(onSea):
            onSea = False
        
        ticket = 0
        nowday = dolScript.getSailDay(proc)
        count = 0
        cos, sin = dolScript.getAngleT(proc)
        cos = -cos
        sin = -sin
        while(nowday < day):
            if(not dolScript.isOnline(proc)):
                log("断线了")
                beep("警告", "断线了")
                return
            while(ticket < ticketnum):
                if(not dolScript.isOnline(proc)):
                    log("断线了")
                    break
                
                log("open ticket")
                dolCall.custom_safe(proc, 8)
                ticket += 1
                time.sleep(2)
            if(count % 10 == 0):
                log("Wait day.... Now day = %d" % (nowday))
            count += 1
            time.sleep(2)
            
            if(dolScript.getHP(proc) < 10):
                dolCall.custom_safe(proc, 7)
                time.sleep(2)
            
            if(dolScript.isDead(proc)):
                log('救助')
                dolCall.custom_safe(proc, 4)
                time.sleep(2)    
            
            dolCall.turnT(proc, cos, sin)
            nowday = dolScript.getSailDay(proc)
        while(dolScript.getLocationType(proc) != dolCallEnum.LocType.Dock):
            log("Enter dock")    
            dolCall.enterDoor(proc, cityid)
            time.sleep(1.5)
            
        while(dolScript.getLocationType(proc) != dolCallEnum.LocType.City):
            log("Into city")
            dolCall.move(proc, dolCallEnum.MoveTo.DockPlaza) # 码头广场
            time.sleep(1.5)
            
        dolCall.walk(proc, bossx, bossy)
        dolCall.talk(proc, bossid)
        time.sleep(2)
        dolCall.sellShip(proc, bossid)
        time.sleep(3)
    
    