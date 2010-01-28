# -*- coding: utf-8 -*-
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
            log("move to dock")
            dolCall.move(proc, dolCallEnum.MoveTo.Dock)
            log("moveSea")
            dolCall.moveSea(proc)
            
        if(onSea):
            onSea = False
        
        ticket = 0
        nowday = dolScript.getSailDay(proc)
        count = 0
        
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
                dolCall.custom(proc, 8) #f8 放奖券
                ticket += 1
                time.sleep(2)
            if(count % 10 == 0):
                log("Wait day.... Now day = %d" % (nowday))
            count += 1
            time.sleep(2)
            nowday = dolScript.getSailDay(proc)
        log("Enter dock")    
        dolCall.enterDoor(proc, cityid)
        log("Into city")
        dolCall.move(proc, dolCallEnum.MoveTo.DockPlaza) # 码头广场
        dolCall.walk(proc, bossx, bossy)
        dolCall.talk(proc, bossid)
        time.sleep(2)
        dolCall.sellShip(proc, bossid)
        time.sleep(3)
    
    