# -*- coding: utf-8 -*-
import sys
sys.path.append("..")
from w32 import w32
#from _global import MyList
import helper
from ctypes import *
from dolAddr import ADDR
from enum import QuickKey, ShipState, Sea
import time
import math
import win32gui, win32con

from global_ import *

dolClassName = "Greate Voyages Online Game MainFrame"



def getHP(proc):
    '''
    获取当前HP
    return int
    '''
    return getInt(proc, ADDR.HP)

def getHPMax(proc):
    '''
    获取最大HP
    return int
    '''
    return getInt(proc, ADDR.HPMAX)

def getHPRatio(proc):
    '''
    获取HP比率
    return float
    '''
    return float(getHP(proc)) / getHPMax(proc)

def getFatigue(proc):
    '''
    获取疲劳值
    return float
    '''
    return float(getShort(proc, ADDR.FATIGUE)) / 10

def getRoleName(proc):
    '''获取玩家名称 
        return string
    '''
  
    addr = getInt(proc, ADDR.PC_NAME)
    nameLength = getInt(proc, addr - 12)#名字长度的地址（中文字数目）
    
    name = getStringW(proc, addr, nameLength)

    return name
    
    #ReadProcessMemory(procHandle.handle, address, buffer, bufferSize, ctypes.byref(bytesRead))

def getLandPos(proc):
    '''陆地坐标
        return : (x,y)
    '''
    x = getFloat(proc, ADDR.PC_X)
    y = getFloat(proc, ADDR.PC_Y)
    return (x, y)

def getLocation(proc):
    '''获取所在地点
        return string
    '''
        
    addr = getInt(proc, ADDR.LOCATION)
    addr = getInt(proc, addr + 4)
       
    nameLength = getInt(proc, addr - 12)    
    name = getStringW(proc, addr, nameLength)

    return name

def getParty(proc):
    '''获取队伍中人物的ID列表
        return []
        
                        如果没有组队，则返回空列表
    '''    
    addr = getInt(proc, ADDR.PARTY_BASE)
    if(addr == 0):
        return []
    else:
        list = []
        for i in range(5):
            id = getInt(proc, addr + 0xC)
            list.append(id)
            addr = getInt(proc, addr)
            if(addr == 0):
                break
        return list
    
def getQuickKey(proc):
    '''获取快捷键列表
        return []
    '''
    list = MyList()
    for i in range(12):
        index = getInt(proc, ADDR.QUICK_KEY + i*4)
        string = QuickKey[index]
        list.append(unicode(string))
        
    return list

def getSeaPos(proc):
    '''返回海上坐标
        return (x,y)
    '''
    dowhile(isSceneChange, [proc])
    seq = getSeaSeq(proc)
    px, py = Sea[seq][1]
    
    x = getFloat(proc, ADDR.PC_X)
    
    if (x != 0.0 and x != 37000.0):
        x = (x - 2560000.0) / 10000.0 + px
        y = getFloat(proc, ADDR.PC_Y)
        
        y = (y - 2560000.0) / 10000.0 + py
        
        if(x < 0.0 or y < 0.0):
            x = -1.0
        
        return (x,y)
    else:
        return (-1.0, -1.0)
    
def getAngleT(proc):
    '''
    返回人物所面向角度
    return cos, sin
    '''
    cos = getFloat(proc, ADDR.PC_COS)
    #print cos
    sin = getFloat(proc, ADDR.PC_SIN)
    return (cos, sin)


def getAngle(proc):
    '''返回人物所面向角度
        return float
        
        以x轴正方向为0度
        逆时针递增
    '''
    
    
    #print sin
    count = 0
    while(True):
        cos, sin = getAngleT(proc)
        try:
            cosdeg = math.acos(cos) * 180 / math.pi
            sindeg = math.asin(sin) * 180 / math.pi
            break
        except ValueError:
            if(count >= 20):
                print "getAngle Fail! cos = %.5f, sin = %.5f" % (cos, sin)
                return
            count += 1
            time.sleep(0.1)
    
    angle = cosdeg
    if(sindeg > 0):
        angle = 360 - angle
    
    return angle


def getShipState(proc):
    '''返回船只状态列表
        return string
    '''
    value = getInt(proc, ADDR.SHIP_STATE)
    if(value == 0):
        return None
    
    i = 1
    while(i <= 0x2000000):
        if(i & value > 0):
            if(ShipState.has_key(i)):
                return ShipState[i]
            else:
                return None
        i <<= 1
    return None

def getTabAddr(proc, id, addr):
    A = getInt(proc, addr)
    B = getInt(proc, addr + 4)
    newaddr = A + (id // 16 % B) * 4
    addr = getInt(proc, newaddr)
    
    count = 0
    str = ''
    while(addr != 0 and count < 100):
        fid = getInt(proc, addr)
        if(fid == id):
            break;
        addr = getInt(proc, addr + 0x08)
        count += 1
    if(count < 100 and addr > 0):
        return getInt(proc, addr + 4)
    else:
        return 0

def getTabId(proc):
    '''返回TAB所指对象的ID
    return int
    '''
    return getInt(proc, ADDR.TAB_ID)
        
def getTabName(proc):
    '''返回TAB所指对象名称
        return string
    '''
    type = getInt(proc, ADDR.TAB_OBJTYPE)
    id = getInt(proc, ADDR.TAB_ID)
    

    if(type == 0):
        addr = getTabAddr(proc, id, ADDR.TAB_PCBASE)
        
        addr = getInt(proc, addr + 0x3C)
        nameLength = getInt(proc, addr - 12)
        return getStringW(proc, addr, nameLength)
    elif(type == 1):
        addr = getTabAddr(proc, id, ADDR.TAB_STATIC)
        if(addr > 0):
            id = getInt(proc, addr + 0xC)
            
            addr = getTabAddr(proc, id, ADDR.TAB_STATIC2)
            
            if(addr > 0):
                addr = getInt(proc, addr+0xC)
                nameLength = getInt(proc, addr -12)
                name = getStringW(proc, addr, nameLength)
                return name
            
        return ''
    else:
        return ''

def getLandFollow(proc):
    '''获取陆地跟随的ID
        return int
    '''
    return getInt(proc, ADDR.LAND_FOLLOW)

def getSeaFollow(proc):
    '''获取海洋跟随的ID
        return int
    '''
    return getInt(proc, ADDR.SEA_FOLLOW)

def getMousePos(hwnd, x, y):
    '''获取鼠标点击的位置，用于TAB对话框
        (返回值为Client坐标，非Window坐标)
        return (x,y)
    '''
    if(x < 0 or x > 4 or y < 0 or y > 4):
        return None
    
    (left, top, right, bottom) = win32gui.GetClientRect(hwnd)
    
    button = (36,20)
    gap = (4,4)
    rect = (-171, -251)
    
    pos = (right + rect[0] + button[0] / 2 + x * (button[0]+gap[0]),
           bottom + rect[1] + button[1] / 2 + y * (button[1]+gap[0]))
    return pos

def getTabNum(proc):
    '''获取选择框的按钮数目(包含关闭按钮)
        如果无打开TAB选择框，(包括tab选中但未按回车)
    return int
    '''
    return getInt(proc, ADDR.TAB_NUM)
    
def getPCID(proc):
    '''获取玩家ID
    return int
    '''
    return getInt(proc, ADDR.PC_ID)
            
def isSceneChange(proc):
    '''是否场景切换
        return bool
    '''
    return getInt(proc,ADDR.SCENE_CHANGE) != 0         
    

def isBusy(proc):
    '''是否鼠标忙
        return bool
    '''
    return getInt(proc,ADDR.MOUSE_BUSY) != 0

def isOnline(proc):
    '''是否在线
    return bool
    '''
    return getInt(proc, ADDR.PC_STATE) == 1

class UnrecoverableException(Exception):
    pass

def isNormal(proc):
    '''是否正常，可执行命令的状态
    == 在线 && !鼠标忙 && !切换场景
    '''
    if(not isOnline(proc)):
        raise UnrecoverableException('diconnected')
    
    return isOnline(proc) and (not isBusy(proc)) and (not isSceneChange(proc))

def getLocationType(proc):
    '''
    获取所在地方类型
    return byte
    '''
    return getByte(proc, ADDR.LOCTYPE)

def getSeaSeq(proc):
    '''
    获取海域序号
    return byte
    '''
    return getByte(proc, ADDR.SEASEQ)

def isAutoSail(proc):
    '''
    是否自动航行
    return bool
    '''
    return getByte(proc, ADDR.AUTO_SAIL) == 1

def getCombat(proc):
    '''
    获取战斗状态
    '''
    return getInt(proc, ADDR.COMBAT_STATE)

def getSkill(proc):
    '''
    获取使用技能状态
    (数目， [技能1ID, 技能2ID, 技能3ID])
    '''
    addr = getInt(proc, ADDR.SKILL_BASE)
    addr = getInt(proc, addr+0x20)
    
    num = getInt(proc, addr + 0x38)
    id1 = getInt(proc, addr + 0xC)
    id2 = getInt(proc, addr + 0x14)
    id3 = getInt(proc, addr + 0x1C)
    
    return (num, [id1, id2, id3])

def getWeather(proc):
    '''
    天气 
    晴天= 0, 2
    雨天 = 0x20
    大雨 = 0x24 ??
    暴风雨 = 0x48, 0x42, 0x41
    阴天 = 0x90 ??
    '''
    return getByte(proc, ADDR.WEATHER)

def isBadWeather(proc):
    weather = getWeather(proc)
    return weather >= 0x41 and weather <= 0x48 

def getSailState(proc):
    '''
    获取帆位
    0-4
    '''
    return getInt(proc, ADDR.SAIL_STATE)

def getSailDay(proc):
    '''
    航行天数
    '''
    return getInt(proc, ADDR.SAIL_DAY)

def getTide(proc):
    '''
    潮流
    '''
    return getByte(proc, ADDR.TIDE)

def getWave(proc):
    '''
    浪高
    '''
    return getByte(proc, ADDR.WAVE)


def getNPC(proc):
    '''
    获取周围一定范围的NPC和玩家
    '''
    
    addr = getInt(proc, ADDR.TAB_PCBASE)
    
    addr_2 = getInt(proc, addr)
    while(addr_2 == 0):
        addr += 4
        addr_2 = getInt(proc, addr)
    for i in range(1000):
        #print "----------------------Round %d -------------------------" % (i)
        #print "addr_2 before = %x" % (addr_2)
        id = getInt(proc, addr_2)
        
        if(id == 0):
            break
        
        namebase = getInt(proc, addr_2 + 4)
        addr_2 = getInt(proc, addr_2 + 8)
        #print "addr_2 after = %x" % (addr_2)
        #print "%x" %( namebase)
        namebase_2 = getInt(proc, namebase + 0x3c)
        #print "%x" % ( namebase_2)
        name = getStringW(proc, namebase_2, 40)
        #name2 = getString(proc, namebase_2, 40)
        #print name2
        #print unicode(name2).encode('gbk')
        #print name.encode('utf-8')
        #print name
        x = getFloat(proc, namebase + 0x3c + 0xe0)
        y = getFloat(proc, namebase + 0x3c + 0xe0 + 0x8)
        #unknown = getFloat(proc, namebase + 0x3c + 0xe0 + 0x4)
        if(x != 0):
            print "id = %8x, name = %s, x = %.3f, y = %.3f" % (id, name,x, y)
        
        
        while(addr_2 == 0):
            addr += 4
            addr_2 = getInt(proc, addr)
            #print "addr_2 Adjust = %x" % (addr_2)

def isCustomOpen(proc):
    return getInt(proc, ADDR.BOOL_CUSTOM) != 0

def readLog(proc, searchDepth = 9999):
    addr = ADDR.LOG_INFO
    
    logList = []
    content = ADDR.LOG_CONTENT
    base = getInt(proc, content)
    for i in range(searchDepth):
        addr = getInt(proc, addr+4)
        offset = getInt(proc, addr + 12)
        wordNum = getInt(proc, addr + 20)
        s = getStringW(proc, base + offset*2, wordNum)
        logList.append(s)
        #print s
        
        addr = getInt(proc, addr + 4)
        if(addr == 0):
            break
    return logList

def inLog(proc, sub, searchDepth = 3):
    logList = readLog(proc, searchDepth)
    for log in logList:
        #print log
        if(log.find(sub) != -1):
            
            return True
    return False

def getToRead(proc):
    '''
    获取将要读的书的序号
    return int
    '''
    addr = getInt(proc, ADDR.MAP_BASE)
    if(addr != 0):
        return getByte(proc, addr + 0x90)
    return -1

def isReading(proc):
    '''
    是否在读书
    return bool
    '''
    addr = getInt(proc, ADDR.MAP_BASE)
    #print 'isReading(): addr = %x' % (addr)
    if(addr != 0):
        status = getByte(proc, addr + 0x196)
        print "reading status = %x" % (status)
        return status != 14
    
    return False

def isDialogOpen(proc):
    '''
    是否對話框已開啟
    return bool
    '''
    return getInt(proc, ADDR.DIALOG) != 0

def getSailor(proc):
    '''
    水手数
    '''
    return getShort(proc, ADDR.SAILOR)

def getShipHP(proc):
    '''
    船耐久
    '''
    return getInt(proc, ADDR.SHIP_HP)

def isDead(proc):
    '''
    是否遇难
    return bool
    '''
    return getShipHP(proc) == 0 or getSailor(proc) == 0 

def getReportSeq(proc):
    '''
    获取报告时学科序号
    '''
    addr = getInt(proc, ADDR.DIALOG)
    if(addr != 0):
        seq = getByte(proc, addr + 0x6BC)
        return seq
    return -1

def getMoney(proc):
    '''
    获取金钱数目
    '''
    return getInt(proc, ADDR.MONEY)

#===============================================================================
# main相关函数
#===============================================================================

def selfTest(proc):
    '''基本信息自检
    '''
    index = 0
    strList = ADDR.getIntStr()
    for addr in ADDR.getIntList():
        #print '%x' % addr
        print strList[index] % ( getInt(proc, addr))
        index += 1
    
    index = 0
    strList = ADDR.getShortStr()
    for addr in ADDR.getShortList():
        #print '%x' % addr
        print strList[index] % ( getShort(proc, addr))
        index += 1
        
def getDolHwndList():
    '''获取所有大航海OL的窗口句柄
    return []
    '''
    winHelper = helper.WindowHelper()
    return winHelper.getWindowListByClassName(dolClassName)
    
if __name__ == "__main__":
    procHelper = helper.WindowHelper()
    dolProcList = procHelper.getProcListByClassName(dolClassName)
    
    if(len(dolProcList) <= 0):
        print '没有大航海OL进程'
    else:
        pro = dolProcList[0]
        print pro.handle

        print getRoleName(pro)
        selfTest(pro)
        print '忙? %s' % (isBusy(pro))
        print '在线? %s' % (isOnline(pro))
        print '地点 = %s' % (getLocation(pro))
        print '队伍列表 = %s' % (getParty(pro))
        #print '快捷键 = %s' % (getQuickKey(pro))
        print '角度 = %s' % (getAngle(pro))
        print '陆地跟随 = %d' % (getLandFollow(pro))
        print '正常 = %s' % (isNormal(pro))
        print '所在地方类型 = %x' % (getLocationType(pro))
        print '海域序号 = %x' % (getSeaSeq(pro))
        print '自动航行 = %s' % (isAutoSail(pro))
        print getSkill(pro)
        print 'hp比率 = %s' % (getHPRatio(pro))
        print '疲劳 = %s' % (getFatigue(pro))
        print '天气 = %x' %(getWeather(pro))
        print '航行状态 = %s' %(getShipState(pro))
        print '帆位 = %d' % (getSailState(pro))
        print '潮流 = %d' % (getTide(pro))
        print '浪 = %d' % (getWave(pro))
        print 'TAB ID = %#x' % (getTabId(pro))
        print 'TAB对象 = %s<end>' % (getTabName(pro))
        print '坐标 = %d, %d' % (getLandPos(pro))
        print '自定义栏开启? = %s' % (isCustomOpen(pro))
        print '海上坐标 = %d, %d' % (getSeaPos(pro))
        print '方向 = %.3f, %.3f' % (getAngleT(pro))
        print '准备读的书是: %d' % (getToRead(pro))
        sub = '未能發現任何物品'
        print '%s 是否在log中 : %s' % (sub, inLog(pro, sub))
        print '是否在讀書: %s' % (isReading(pro))
        print '是否對話框已開啟: %s' % (isDialogOpen(pro))
        print inLog(pro, '得到了教會宗教畫的地圖', 3)
        print '水手数 = %d' % (getSailor(pro))
        print '船耐久 = %d' % (getShipHP(pro))
        print '金钱 = %d' % (getMoney(pro))

        print "%s %s" % (getInt(pro, ADDR.DIALOG) != 0, not isReading(pro))
        print "%x" % (win32con.MB_ICONINFORMATION)
        print "%x" % (win32con.MB_SETFOREGROUND)
        print "%x" % (win32con.MB_ICONINFORMATION | win32con.MB_TOPMOST | win32con.MB_SYSTEMMODAL | win32con.MB_SETFOREGROUND)
        print inLog(pro, '未能發現任何物品')
        print not inLog(pro, '開鎖失敗了')
        
        #readLog(pro)
#        while(True):
#            print '海洋坐标: x=%.3f, y=%.3f' % getSeaPos(pro, (0x400, 0xbff))
#            print '陆地坐标: x=%.3f, y=%.3f' % getLandPos(pro)
#            print '场景切换?: %s' % (isSceneChange(pro))
            #print '忙? %s' % (isBusy(pro))
#            time.sleep(0.01)
            
    
    
    
    

     
    