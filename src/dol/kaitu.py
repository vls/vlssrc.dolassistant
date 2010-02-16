# -*- coding: utf-8 -*-
import dolCall, dolScript
import kaituDta
import time
from global_ import log, dowhile, dountil, beep, TextLogger
import sys
sys.path.append('..')
import dll
import helper
import win32con


def kaitu(proc, dtaClass):
    hlper = helper.ProcessHelper()
    hwnd = hlper.getHwndByProc(proc)
    assert isinstance(dtaClass, kaituDta.kaituDtaBase)
    
    def __printLastLog(depth = 5):
        print 'last log'
        logList = dolScript.readLog(proc, depth)
        for log in logList:
            print log
    
    def __stopSkill():
        while(True):
            sc, _ = dolScript.getSkill(proc)
            if(sc != 0):
                dll.Mouse('LClick', hwnd, 780, 290)
                time.sleep(0.5)
                dll.Key('KeyClick', hwnd, win32con.VK_RETURN)
                time.sleep(1)
            else:
                break
    
    while(True):
        while(True):
            x, y = dtaClass.kaiPos
            dolCall.walk(proc, x, y)
            
            while(dolScript.getHP(proc) < 20):
                dolCall.custom_safe(proc, 7)
                time.sleep(1)
            
            dolCall.custom_safe(proc, 4)
            
            statAddr = 0x00B72FB8
            
            statArr = []
            
            while(not dolScript.inLog(proc, '點經驗。', 2) and not dolScript.inLog(proc, '冒險等級上升到', 2) and not dolScript.inLog(proc, '冒險經驗值達到了', 2)):
                
                sub = '這附近好像有什麼東西'
                if(dolScript.inLog(proc, sub, 2)):
                    print '好像有什麼東西， 繼續'
                    dolCall.custom_safe(proc, 4)
                    time.sleep(2)
                if(dolScript.inLog(proc, '未能發現任何物品')):
                    if(not dolScript.inLog(proc, '開鎖失敗了')):    
                        __printLastLog()
                        print "can't find any item"
                        __stopSkill()
                        beep('', '没图了！')
                        
                        return    
                    else:
                        dolCall.custom_safe(proc, 4)
                        
                time.sleep(0.2)
                
                print 'wait ... %d' % (dolScript.getByte(proc, statAddr))
                statArr.append(dolScript.getByte(proc, statAddr))
            print 'final wait ... %d' % (dolScript.getByte(proc, statAddr))
            statArr.append(dolScript.getByte(proc, statAddr))
            
            logger = TextLogger('kaituLog.txt')
            logger.log(repr(statArr))
            
            if(dolScript.inLog(proc, '未能發現任何物品')):
                if(not dolScript.inLog(proc, '開鎖失敗了')):  
                    __printLastLog() 
                    print "can't find any item"
                    __stopSkill() 
                    beep('', '没图了！')
                    return
                else:
                    continue
            __printLastLog()
            break
        
        __stopSkill()
            
        
        x, y = dtaClass.churchOutPos
        dolCall.walk(proc, x, y)
        dolCall.enterDoor(proc, dtaClass.churchOutID)
        
        x, y = dtaClass.reportEnterPos
        dolCall.walk(proc, x, y)
        dolCall.enterDoor(proc, dtaClass.reportEnterID)
        
        x, y = dtaClass.reportPos
        dolCall.walk(proc, x, y)
        bossid = dtaClass.reportNPCID
        
        while(not dolScript.isDialogOpen(proc)):
            dolCall.openDialog(proc, bossid, 0x65)
            time.sleep(0.5)
        dountil(dolScript.isDialogOpen, [proc])
        
        while(dolScript.getReportSeq(proc) != dtaClass.subSeq):
            dll.Key('KeyClick', hwnd, win32con.VK_DOWN)
            time.sleep(0.5)
        
        
        dll.Key('KeyClick', hwnd, win32con.VK_RETURN)
        time.sleep(1)
        while(not dolScript.inLog(proc, '已經做了報告。', 2) and not dolScript.inLog(proc, '點聲望', 2) ):
            
            dll.Key('KeyClick', hwnd, win32con.VK_RETURN)
            time.sleep(1)
        
        dolCall.enterDoor(proc, dtaClass.reportOutID)
        x, y = dtaClass.churchPos
        dolCall.walk(proc, x, y)
        dolCall.enterDoor(proc, dtaClass.churchEnterID)
    
    
def ktMain(proc):
    dta = kaituDta.mei5()
    kaitu(proc, dta)
    
        


