# -*- coding: utf-8 -*-

import dolCall, dolScript, dolLib, dolCallEnum
import time
from global_ import log, dountil
        
        

def gotoCity(proc, cityid, wayPointList):
    
    def isClose(x1, y1):
        x, y = dolScript.getSeaPos(proc)
        return dolLib.distance(x1, y1, x, y) <= 10
    
    print 'Go to City %x' % (cityid)
    while(dolScript.getLocationType(proc) == dolCallEnum.LocType.Dock):
        dolCall.moveSea(proc)
        time.sleep(0.5)
    time.sleep(2)
    for x1, y1 in wayPointList:
        x, y = dolScript.getSeaPos(proc)
        log('Going to %d, %d' % (x1, y1))
        log('My pos = %d, %d' % (x, y))
        while(dolLib.distance(x1, y1, x, y) > 5):
            log('---Going to %d, %d' % (x1, y1))
            dolLib.turnPos(proc, x1, y1)
            time.sleep(2)
            
            state = dolScript.getSailState(proc)
            if(state < 4):
                dolCall.sail(proc, 4)
                time.sleep(2)
            
            if(not isClose(x1, y1) and not dolScript.isSceneChange(proc) and not dolScript.isAutoSail(proc) and dolScript.getHP(proc) >= 10):
                dolCall.custom_safe(proc, 1)
                time.sleep(2)
                
            sCount, sList = dolScript.getSkill(proc) 
    
            if(not isClose(x1, y1) and not dolScript.isSceneChange(proc) and sCount != 3 and 75 not in sList): #75 == 警戒
                log("发动警戒技能") 
                dolCall.custom_safe(proc, 3)#f3 警戒
                time.sleep(2)
            
            
            
            while(not isClose(x1, y1) and dolScript.getHPRatio(proc) < 0.4):
                if(not dolScript.isOnline(proc)):
                    break
                    
                hp1 = dolScript.getHP(proc)
                log("要补行动力, 行动力 = %d" % (hp1))
                dountil(dolScript.isNormal, [proc])
                
                dolCall.custom_safe(proc, 7) #f7 要设置为料理
                time.sleep(2)
                hp2 = dolScript.getHP(proc)
                log("吃了一个料理, 行动力 = %d" % (hp2))
                if(hp1 == hp2):
                    time.sleep(5)
                time.sleep(0.2)
            x, y = dolScript.getSeaPos(proc)
            print "Now in (%d, %d), distance to (%d, %d) is %d" % (x,y, x1, y1, dolLib.distance(x1, y1, x, y))
    dolCall.sail(proc, 0)
    dolCall.enterDoor(proc, cityid)
            
        
    