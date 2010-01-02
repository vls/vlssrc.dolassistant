# -*- coding: utf-8 -*-
from w32 import w32
from _global import MyList
import helper
from ctypes import *
from dolAddr import ADDR
from enum import QuickKey, ShipState, Sea
import time
import math

dolClassName = "Greate Voyages Online Game MainFrame"

def getStringW(proc, addr, length):
    buf = c_wchar_p(' ' * (length))
    bytesRead = c_ulong(0)
    w32.ReadProcessMemory(proc.handle, addr, buf, length * 2, byref(bytesRead))
    return buf.value
    

def getFloat(proc, addr):
    '''获取float
        return float
    '''
    buf = c_float(0)
    bytesRead = c_ulong(0)
    bufferSize = 8    
    w32.ReadProcessMemory(proc.handle, addr, byref(buf), bufferSize, byref(bytesRead))
    return buf.value
    
def getInt(proc, addr):
    '''获取4字节的内容
        return int
    '''
    buf = c_int(0)
    bytesRead = c_ulong(0)
    bufferSize = 4    
    w32.ReadProcessMemory(proc.handle, addr, byref(buf), bufferSize, byref(bytesRead))
    return buf.value

def getShort(proc, addr):
    '''获取两字节内容
        return short int
    '''
    buf = c_int(0)
    bytesRead = c_ulong(0)
    bufferSize = 2    
    w32.ReadProcessMemory(proc.handle, addr, byref(buf), bufferSize, byref(bytesRead))
    return buf.value
    
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

def getSeaPos(proc, point):
    '''返回海上坐标
        return (x,y)
    '''
    
    x = getFloat(proc, ADDR.PC_X)
    if (x != 0.0 and x != 37000.0):
        x = (x - 2560000.0) / 10000.0 + point[0]
        y = getFloat(proc, ADDR.PC_Y)
        y = (y - 2560000.0) / 10000.0 + point[1]
        
        if(x < 0.0 or y < 0.0):
            x = -1.0
        
        return (x,y)
    else:
        return (-1.0, -1.0)

def getAngle(proc):
    '''返回人物所面向角度
        return float
        
        以x轴正方向为0度
        逆时针递增
    '''
    
    cos = getFloat(proc, ADDR.PC_COS)
    sin = getFloat(proc, ADDR.PC_SIN)
    
    cosdeg = math.acos(cos) * 180 / math.pi
    sindeg = math.asin(sin) * 180 / math.pi
    
    angle = cosdeg
    if(sindeg > 0):
        angle = 360 - angle
    
    return angle

def getShipState(proc):
    '''返回船只状态列表
        return []
    '''
    list = MyList()
    value = getInt(proc, ADDR.SHIP_STATE)
    i = 1
    while(i <= 0x2000000):
        if(i & value > 0):
            list.append(ShipState[i])
    return list

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
    #if(x < 0 or x > 4 or )
    pass
    
            

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
        print '地点 = %s' % (getLocation(pro))
        print '队伍列表 = %s' % (getParty(pro))
        print '快捷键 = %s' % (getQuickKey(pro))
        print '角度 = %s' % (getAngle(pro))
        print 'TAB对象 = %s<end>' % (getTabName(pro))
        print '陆地跟随 = %d' % (getLandFollow(pro))
#        while(True):
#            print '海洋坐标: x=%.3f, y=%.3f' % getSeaPos(pro, (0x400, 0xbff))
#            print '陆地坐标: x=%.3f, y=%.3f' % getLandPos(pro)
#            print '场景切换?: %s' % (isSceneChange(pro))
#            time.sleep(0.01)
            
    
    
    
    

     
    