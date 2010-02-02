# -*- coding: utf-8 -*-
import dolCallEnum
from ctypes import *
import win32con, win32api, win32process, win32event, win32security
import random, math
from dolData import *
from heapq import heappush, heappop
import time
from dolAddr import ADDR
import dolScript
import dolCallCmd
import dolCallAddr
from global_ import *

from dolCallEnum import SellInfo, BuyInfo, ToBuy, buyCountDict


area = dolCallCmd.TW
CALLADDR = dolCallAddr.TW


changeDelay = 2 # 切换场景类的操作的等待延时
CMDSIZE = 1024
PARASIZE = 24

class MemException(Exception):
    pass




def Clean(proc):
    win32api.CloseHandle(proc)


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

def isNormal(proc):
    '''是否正常，可执行命令的状态
    == 在线 && !鼠标忙 && !切换场景
    '''
    flag = isOnline(proc)
    print isBusy(proc)
    flag2 = not isBusy(proc)
    flag3 = not isSceneChange(proc)
    print "isNormal %s %s %s" % (flag, flag2, flag3)
    return flag and flag2 and flag3

def writeCmd(proc, cmdList):
    '''
    注意：如果成功，需要使用者自行释放内存
    '''
    size = CMDSIZE
    
    assert len(cmdList) == size
    cmd = (c_ubyte * size)()
    
    for i in range(size):
        cmd[i] = cmdList[i]
        
    buf = VirtualAllocEx(proc.handle, None, size, win32con.MEM_COMMIT, win32con.PAGE_READWRITE)
    if(buf == 0):
        raise MemException('VirtualAllocEx Fails')
    
    written = c_long(0) 
    ret = WriteProcessMemory(proc.handle, buf, byref(cmd), size, byref(written))
    
    if(written.value != size):
        ret = VirtualFreeEx(proc.handle, buf, 0, win32con.MEM_RELEASE)
        if (ret == 0):
            raise MemException("Release memory failed!")
        raise MemException("WriteProcessMemory() does NOT write the complete command!")
    if(ret == 0):
        ret = VirtualFreeEx(proc.handle, buf, 0, win32con.MEM_RELEASE)
        if (ret == 0):
            raise MemException("Release memory failed!")
        raise MemException('WriteProcessMemory() fails!')
    
    return buf

def writePara(proc, cPara):
    '''
    注意：如果成功，需要使用者自行释放内存
    '''
    #
    size = sizeof(cPara)
        
    buf = VirtualAllocEx(proc.handle, None, size, win32con.MEM_COMMIT, win32con.PAGE_READWRITE)
    if(buf == 0):
        raise MemException('VirtualAllocEx Fails')
    
    written = c_long(0) 
      
    ret = WriteProcessMemory(proc.handle, buf, byref(cPara), size, byref(written))
    
    if(written.value != size):
        ret = VirtualFreeEx(proc.handle, buf, 0, win32con.MEM_RELEASE)
        if (ret == 0):
            raise MemException("Release memory failed!")
        raise MemException("WriteProcessMemory() does NOT write the complete command!")
    if(ret == 0):
        ret = VirtualFreeEx(proc.handle, buf, 0, win32con.MEM_RELEASE)
        if (ret == 0):
            raise MemException("Release memory failed!")
        raise MemException('WriteProcessMemory() fails!')
    
    return buf

def execCmd(proc, cmdBuf, paraBuf):
    tHandle, tid = win32process.CreateRemoteThread(proc.handle, None, 0, cmdBuf, paraBuf, 0)
    print "Success! ThreadHandle, ThreadID = %d,%d" %( tHandle, tid)
    
    
    
    
    win32event.WaitForSingleObject(tHandle, -1)
    ret = win32api.CloseHandle(tHandle)
    if(ret == 0):
        raise MemException("Close handle failed!")
    
    ret = VirtualFreeEx(proc.handle, cmdBuf, 0, win32con.MEM_RELEASE)
    if(ret == 0):
        raise MemException("Release memory failed!")
    
    ret = VirtualFreeEx(proc.handle, paraBuf, 0, win32con.MEM_RELEASE)
    if(ret == 0):
        raise MemException("Release memory failed!")
    
    print "Cleaned"
    
def writeMem(proc, addr, writeBuf):
    
    
    
     
    written = c_long(0)
    
    size = sizeof(writeBuf)
    ret = WriteProcessMemory(proc.handle, addr, byref(writeBuf), size, byref(written))
    
    if(written.value != size):
        raise MemException("WriteProcessMemory() does NOT write the complete content!")
    if(ret == 0):
        raise MemException('WriteProcessMemory() fails!')


def __openDialog(proc, bossid, dialogID):
    '''
    开启游戏的对话框
    '''
    cpara = (c_ubyte * PARASIZE)()
    ip = cast(cpara, POINTER(c_int))
    ip[0] = bossid
    ip[1] = 0
    ip[2] = dialogID
    
    paraBuf = writePara(proc, cpara)
    cmdBuf = writeCmd(proc, area.openDialogCmd)
    
    dowhile(isNormal, [proc])
    execCmd(proc, cmdBuf, paraBuf)
    time.sleep(changeDelay)
    
def __translate(proc):
    byteList = [0x61,0x84,0x04,0x84,0x52,0x91]
    #byteList = [0x1F,0x67,0x85,0x5F,0xC2,0x53,0x18,0x62,0x84,0x76,0x04,0x54,0x4D,0x4F,0xAA,0x52,0x9B,0x52,0x4B,0x59,0x97,0x65,0x02,0x30]
    byteList.append(0)
    length = len(byteList)
    buf = (c_ubyte * length)()
    print buf
    for i in range(length):
        buf[i] = byteList[i]
    
    addr = writePara(proc, buf)
    print getStringW(proc, addr, 40)
    
    ret = VirtualFreeEx(proc.handle, addr, 0, win32con.MEM_RELEASE)
    if(ret == 0):
        raise MemException("Release memory failed!")

def __gettab(proc):
    print "0x%x" % (dolScript.getTabId(proc))

def __getstr(proc, addr):
    addr = int(addr)
    string =  getStringW(proc, addr, 0x18)
    print string
    print len(string)

#===============================================================================
# Specific functions    
#===============================================================================

def walk(proc, x, y):
    x = float(x)
    y = float(y)
    
    nowx, nowy = dolScript.getLandPos(proc)
    
    while(nowx != x and nowy != y):
        cmdBuf = writeCmd(proc, area.walkCmd)
        
        cpara = (c_ubyte * PARASIZE)()
    
        fpara = cast(cpara, POINTER(c_float))
        #print "x=%f, y=%f" % (x,y)
        fpara[0] = x
        fpara[1] = y
        
        ipara = cast(cpara, POINTER(c_int))
        for i in range(4):
            ipara[i+2] = getInt(proc, area.walkSeqAddrList[i])
            
        #=======================================================================
        # for i in range(24):
        #    print "para = %x" % (cpara[i])
        #=======================================================================
            
            
        paraBuf = writePara(proc, cpara)
        dowhile(isNormal, [proc])
        execCmd(proc, cmdBuf, paraBuf)
        
        time.sleep(0.2)
        nowx, nowy = dolScript.getLandPos(proc)
        

    
def follow(proc, userid):
    #print len(area.followCmd)
    
    userid = int(userid)
    
    cmdBuf = writeCmd(proc, area.followCmd)
    
    
    cpara = (c_ubyte * PARASIZE)()
    
    for i in range(len(area.followPara)):
        cpara[i] = area.followPara[i]
        
        
    p = cast(cpara, POINTER(c_int))
    #print cpara
    #print p
    
    p[0] = userid    
    
    #high = random.randrange(0x100,0x1FF) << 16
    #p[5] += high
    #print p[4]
    #for i in range(6):
        #print p[i]
    
    #===========================================================================
    # for i in range(24):
    #    print "pp = %x" % (cpara[i])
    #===========================================================================
        
    paraBuf = writePara(proc, cpara)
    dowhile(isNormal, [proc])
    execCmd(proc, cmdBuf, paraBuf)
    
def seafollow(proc, userid):
    '''
    海上跟随
    '''
    userid = int(userid)
    
    cmdBuf = writeCmd(proc, area.seaFollowCmd)  
    
    cpara = (c_ubyte * PARASIZE)()
    for i in range(len(area.seaFollowPara)):
        cpara[i] = area.seaFollowPara[i]
    
    ip = cast(cpara, POINTER(c_int))
    ip[0] = userid
    
    paraBuf = writePara(proc, cpara)
    dowhile(isNormal, [proc])
    execCmd(proc, cmdBuf, paraBuf)
    
def move(proc, moveto):
    '''
    从码头进入城市，或者从城市进入码头
    '''
    
    
    userid = dolScript.getPCID(proc)
    moveto = int(moveto)
        
    
    cpara = (c_ubyte * PARASIZE)()
    ip = cast(cpara, POINTER(c_int))
    ip[0] = userid
    ip[1] = moveto
    
    
    paraBuf = writePara(proc, cpara)
        
    cmdBuf = writeCmd(proc, area.moveCmd)
    dowhile(isNormal, [proc])
    execCmd(proc, cmdBuf, paraBuf)
    time.sleep(changeDelay)

def moveSea(proc):
    '''
    出航
    '''
    
    userid = dolScript.getPCID(proc)
    
    cpara = (c_ubyte * PARASIZE)()
    ip = cast(cpara, POINTER(c_int))
    ip[0] = userid
    ip[1] = 0x41d34c
    
    paraBuf = writePara(proc, cpara)
        
    cmdBuf = writeCmd(proc, area.moveToSeaCmd)
    dowhile(isNormal, [proc])
    execCmd(proc, cmdBuf, paraBuf)
    time.sleep(changeDelay)
    
def turn(proc, deg):
    '''
    以x轴正方向为0度，逆时针
    '''
    deg = float(deg)
    cos = math.cos(math.radians(deg))
    sin = -math.sin(math.radians(deg))
    
    
    cpara = (c_ubyte * PARASIZE)()
    fp = cast(cpara, POINTER(c_float))
    fp[0] = cos
    fp[1] = sin
    
    
    paraBuf = writePara(proc, cpara)
    cmdBuf = writeCmd(proc, area.turnCmd)
    dowhile(isNormal, [proc])
    execCmd(proc, cmdBuf, paraBuf)

def custom(proc, num):
    '''
    使用自订栏
    '''
    num = int(num)
    if( num < 1 or num > 8):
        print 'Invalid num'
        return

    num -= 1
    
    cpara = (c_ubyte * PARASIZE)()
    ip = cast(cpara, POINTER(c_int))
    ip[0] = num
    ip[1] = 0x41e868
    
    #===========================================================================
    # ip[2] = random.randrange(0x3f0000, 0x018effff)
    # ip[3] = random.randrange(0x3f0000, 0x018effff)
    # ip[4] = random.randrange(0x3f0000, 0x0199ffff)
    # ip[5] = random.randrange(0x3f0000, 0x018effff)
    #===========================================================================
    
    paraBuf = writePara(proc, cpara)
    cmdBuf = writeCmd(proc, area.customCmd)
    dowhile(isNormal, [proc])
    execCmd(proc, cmdBuf, paraBuf)
    
def enterD(proc):
    '''
    进港, 进门, 出门
    '''
    addr = getInt(proc, ADDR.TAB_STATIC)
    print "addr = %x" % (addr)
    
    tarx = getFloat(proc, ADDR.PC_X)
    tary = getFloat(proc, ADDR.PC_Y)
    
    
    
    heap = []
    for i in range(10):
        value = getInt(proc, addr)
        while(value == 0):
            addr += 4
            value = getInt(proc, addr)
            print "value = %x, addr = %x" % (value, addr)
        addr += 4
    
        
        addr_2 = value
        prevalue = getInt(proc, addr_2)
        value = getInt(proc, addr_2+4)
        print "prevalue = %x, value = %x, addr_2 = %x" %(prevalue, value, addr_2)
        while(value != 0):
            addr_2 += 4
            prevalue = value
            value = getInt(proc, addr_2+4)
            print "prevalue = %x, value = %x, addr_2 = %x" %(prevalue, value, addr_2)
            
        
        cityid = getInt(proc, prevalue + 4)
        
        if(cityid == 0):
            break
        
        x = getFloat(proc, prevalue + 0x10)
        y = getFloat(proc, prevalue + 0x18)
        p = Pos(cityid, tarx, tary, x, y)
        
        if(x != 0 and y != 0):
            heappush(heap, p)
        
        print "%x %.4f %.4f dis = %d" % ( cityid, x, y, p.dis)
    near = heappop(heap)
    print "x = %.4f, y= %.4f" % (tarx,tary)
    print "the nearest door is %x %d" % (near.id, near.dis)
     
    
    enterDoor(proc, near.id)

def enterDoor(proc, did):
    '''
    '''
    
    cpara = (c_ubyte * PARASIZE)()
    ip = cast(cpara, POINTER(c_int))
    ip[0] = did
    ip[1] = 0x41d34c
    

    
    paraBuf = writePara(proc, cpara)
    cmdBuf = writeCmd(proc, area.enterDCmd)
    
    dowhile(isNormal, [proc])
    execCmd(proc, cmdBuf, paraBuf)
    time.sleep(changeDelay)


def sail(proc, state):
    '''
    升降帆
    '''
    state = int(state)
    assert state >= 0 and state <= 4
    
    
    cpara = (c_ubyte * PARASIZE)()
    ip = cast(cpara, POINTER(c_int))
    ip[0] = state
    ip[1] = 0x41fd08
    
    #===========================================================================
    # ip[2] = random.randrange(0x026bFFFF, 0x02830000)
    # ip[3] = random.randrange(0x027d0000, 0x0283FFFF)
    # ip[4] = random.randrange(0x026bFFFF, 0x02830000)
    # ip[5] = random.randrange(0x027d0000, 0x0283FFFF)
    #===========================================================================
    
    paraBuf = writePara(proc, cpara)
    cmdBuf = writeCmd(proc, area.sailCmd)
    
    dowhile(isNormal, [proc])
    execCmd(proc, cmdBuf, paraBuf)
    




def __isOpened(proc):
    '''
    开了对话框？
    (存疑)
    '''
    addr = getInt(proc, ADDR.SKILL_BASE)
    #print "%x" %(addr)
    addr = getInt(proc, addr)
    addr = getInt(proc, addr + 8)
    value = getInt(proc, addr + 0xC)
    
    return value != 0

def __getSellPara(proc):
    '''
    获取卖船的某个参数
    '''
    addr = getInt(proc, CALLADDR.DIALOG)
    print "addr = %x" % (addr)
    print "after adjust = %x" %(addr + 0x5e8)
    addr = getInt(proc, addr + 0x5e8)
    
    print "addr = %x" % (addr)
    print "after adjust = %x" %(addr + 0xe8)
    value2 = getInt(proc, addr + 0xe8)
    print "value2 = %x" % (value2)
    return value2

def sellShip(proc, bossid):
    '''
    卖船
    '''
    
    bossid = int(bossid)
     
    
    if(not __isOpened(proc)):
        
        
        __openDialog(proc, bossid, 0x53)
    
        while(True):
            if(__isOpened(proc)):
                print "Open finished!"
                break      
            print "Wait..."      
            time.sleep(0.2)
    
    para2 = __getSellPara(proc)
    
    
    cpara = (c_ubyte * PARASIZE)()
    ip = cast(cpara, POINTER(c_int))
    ip[0] = bossid
    ip[1] = para2
    ip[2] = 0x53
    
    paraBuf = writePara(proc, cpara)
    cmdBuf = writeCmd(proc, area.sellShipCmd)
    
    time.sleep(4) #sleep for sell the correct ship, but it doesn't works....
    dowhile(isNormal, [proc])
    execCmd(proc, cmdBuf, paraBuf)
    
def talk(proc, tarid):
    '''
    与npc对话
    '''
    tarid = int(tarid)
    
    
    cpara = (c_ubyte * PARASIZE)()

    
    ip = cast(cpara, POINTER(c_int))
    ip[0] = tarid
    
    paraBuf = writePara(proc, cpara)
    cmdBuf = writeCmd(proc, area.talkCmd)
    
    dowhile(isNormal, [proc])
    execCmd(proc, cmdBuf, paraBuf)
    
def buildShip(proc, shipid, woodid, storage, bossid):
    '''
    买船
    '''
    shipid = int(shipid)
    woodid = int(woodid)
    storage = int(storage)
    bossid = int(bossid)
    
    
    cpara = (c_ubyte * PARASIZE)()

    
    ip = cast(cpara, POINTER(c_int))
    ip[0] = shipid
    ip[1] = woodid
    ip[2] = storage
    ip[3] = bossid
    ip[4] = 0x0206
    
    paraBuf = writePara(proc, cpara)
    cmdBuf = writeCmd(proc, area.buildShipCmd)
    
    dowhile(isNormal, [proc])
    execCmd(proc, cmdBuf, paraBuf)



def __getFoodMenu(proc):
    
    addr = getInt(proc, CALLADDR.DIALOG)
    
    while(addr == 0):
        print 'Wait...'
        time.sleep(0.5)
        addr = getInt(proc, CALLADDR.DIALOG)
    
    seq = getShort(proc, addr + 0x604)
    
    seqAddr = CALLADDR.SEQ
    
    status = getInt(proc, seqAddr)
    print "%x" % (status)
    
    if(seq != status):
        writeMem(proc, seqAddr, c_int(seq))
        
        status = getInt(proc, CALLADDR.SEQ)
        print "%x" % (status)
    
    
    addr = getInt(proc, addr + 0x5ec)
    
    foodList = []
    
    while(addr != 0):
        print "addr = %x" % (addr)
        food = getInt(proc, addr + 8)
        foodList.append(food)
        addr = getInt(proc, addr)
        print "food = %x, nextaddr = %x" % (food, addr)
    
    return (seq, foodList)

def eat(proc, bossid, water, food):
    
    bossid = int(bossid)
    water = int(water)
    food = int(food)

    
    __openDialog(proc, bossid, 0x70)
    
    
    seq, foodList = __getFoodMenu(proc)
    
    foodLen = len(foodList)
    if(water < 0 or water > foodLen or food < 0 or food > foodLen):
        print "Invalid parameter"
        return
    
    waterid = None
    if(water == 0):
        waterid = 0
    else:
        waterid = foodList[water - 1]
    
    foodid = None
    if(food == 0):
        foodid = 0
    else:
        foodid = foodList[food - 1]
    
    
    
    cpara = (c_ubyte * PARASIZE)()
    ip = cast(cpara, POINTER(c_int))
    ip[0] = seq
    ip[1] = foodid
    ip[2] = waterid
    ip[3] = bossid
    
    paraBuf = writePara(proc, cpara)
    cmdBuf = writeCmd(proc, area.eatCmd)
    
    dowhile(isNormal, [proc])
    execCmd(proc, cmdBuf, paraBuf)



def __getBuyCount(value):
    return dolCallEnum.buyCountDict[value]



def __split(info, tobuyNum):
    tupleList = []
    
    #print "in __split : tobuyNum = %d" % (tobuyNum)
    if(tobuyNum >= info[2][1]):    
        slot = info[2][0]
        times = tobuyNum // info[2][1]
        
        tupleList.append((slot, times, info[2][2]))
        
        remain = tobuyNum % info[2][1]
    else:
        remain = tobuyNum
    #print "in __split : remain = %d" % (remain)    
    if(remain > 0 and remain >= info[0][1]): #还有剩余要买 且 是最小slot可以cover的
        if(info[1][1] % info[0][1] == 0): #如果第一个slot 是包含第二个slot的约数
            slot = info[0][0]
            times = remain // info[0][1]
            tupleList.append((slot, times, info[0][2]))
            
        else: #其实只有2,5,10这种情况 slot = [1,2,3]
            
            tdict = {
                    2:[(1, 1)],
                    3:[(1, 1)],
                    4:[(1, 2)],
                    5:[(2, 1)],
                    6:[(1, 3)],
                    7:[(1, 1), (2, 1)],
                    8:[(1, 4)],
                    9:[(1, 2), (2, 1)],
                    }
            
            tList = tdict[remain]
            for slot,times in tList:
                if(slot == 1):
                    tupleList.append((slot, times, info[0][2]))
                elif(slot == 2):
                    tupleList.append((slot, times, info[1][2]))
        
    return tupleList    

def __testbuy(proc):
    xd_trade = 25166277
    bossid = xd_trade
    print "bossid = %x" % (bossid)
    buy(proc, bossid, [0xFFF, -1, 0xFFF, -1, 0xFFF, -1, -1])

def buy(proc, bossid, buyList):
    
    #===========================================================================
    # seqAddr = 0xafd398
    # print "%x" % (getByte(proc, seqAddr))
    #===========================================================================
    
    #bossid = 0x18005d6
    bossid = int(bossid)
    
    __openDialog(proc, bossid, 0x4C)
    
    addr = getInt(proc, CALLADDR.DIALOG)
    while(addr == 0):
        print 'wait...'
        time.sleep(0.5)
        addr = getInt(proc, CALLADDR.DIALOG)
    
    goodaddr = addr + 0x628
        
    count = getInt(proc, goodaddr)
    print "good's count = %d" % (count)
    
    if(count != len(buyList)):
        print 'Invalid *buylist*, whose length is not equal to the count of selling '
        return
    
    #print "a number = %x" % (getInt(proc, goodaddr - 0x40))
    
    goodList = []
    loadAddr = addr + 0x600
    maxLoadAddr = loadAddr + 8
    
    load = getShort(proc, loadAddr)
    maxLoad = getShort(proc, maxLoadAddr)
    
    if(load == maxLoad):
        print "the ship is full!"
        return
    
    addr = getInt(proc, goodaddr + 0x40)
    while(addr != 0):
        tempaddr = getInt(proc, addr + 8)
        goodid = getInt(proc, tempaddr + 8)
        num1 = getInt(proc, tempaddr + 8 + 4)
        namelen = getInt(proc, num1 - 8)
        
        name = getStringW(proc, num1, namelen)
        
        remain = getShort(proc, tempaddr + 0x18)
        addr = getInt(proc, addr)
        print "goodId = %x, name = %s, remain = %d" % (goodid, name, remain)
        go = BuyInfo()
        go.id = goodid
        go.name = name
        go.remain = remain
        goodList.append(go)
    
    addr = getInt(proc, goodaddr - 4)
    addr += 0x24
    for i in range(count):
        
        
        dataaddr = getInt(proc, addr + i * 0x40)
        
        buyCount_1 = getByte(proc, dataaddr + 0x18)
        buyCount_2 = getByte(proc, dataaddr + 0x38)
        buyCount_3 = getByte(proc, dataaddr + 0x58)
        
        buyCount = [buyCount_1, buyCount_2, buyCount_3]
        #print buyCount
        realBuyCount = [ __getBuyCount(x) for x in buyCount]
        #print realBuyCount
        
        buyPrice = [getInt(proc, dataaddr + 0x8), getInt(proc, dataaddr + 0x28), getInt(proc, dataaddr + 0x48)]
        #for seq in buySeq:
        #    print "%x" % (seq)
        
        info = tuple(zip(buyCount, realBuyCount, buyPrice)) 
        
        goodList[i].info = info

    tobuyList = MyList()

    for i in range(count):
        remain = goodList[i].remain
        if(remain == 0):
            continue
        
        buyNum = -1
        if(buyList[i] == -1):
            buyNum = 0
        elif(buyList[i] == 0):
            tobuy = ToBuy()
            buyNum = goodList[i].info[0][1]
            if(remain < buyNum):
                continue
            tobuy.id = goodList[i].id
            tobuy.slot = goodList[i].info[0][0] + 0xA300
            tobuy.price = goodList[i].info[0][2]
            tobuy.times = 1
            tobuyList.append(tobuy)
        elif(buyList[i] >= 999):
            #print "in maxbuy : remain = %d" % (remain)
            planList = __split(goodList[i].info, remain)
            #print planList
            #print 
            for slot, times, price in planList:
                tobuy = ToBuy()
                tobuy.id = goodList[i].id
                tobuy.slot = slot + 0xA300
                tobuy.price = price
                tobuy.times = times
                tobuyList.append(tobuy)
        
        else:
            if(remain > buyList[i]):
                buyNum = buyList[i]
            else:
                buyNum = remain
            
            planList = __split(goodList[i].info, buyNum)
            for slot, times, price in planList:
                tobuy = ToBuy()
                tobuy.id = goodList[i].id
                tobuy.slot = slot + 0xA300
                tobuy.price = price
                tobuy.times = times
                tobuyList.append(tobuy)
    print tobuyList
        
    load = getShort(proc, loadAddr)
    maxLoad = getShort(proc, maxLoadAddr)
    
    
    realtobuyList = MyList()
    token = 0
    for tobuy in tobuyList:
        space = buyCountDict[tobuy.slot - 0xA300] * tobuy.times
        
        if(load + token + space <= maxLoad):
            print "space = %d, token = %d, load= %d, max = %d" % (space, token, load, maxLoad)
            realtobuyList.append(tobuy)
            token += space
    print 
    print realtobuyList
      
    
    addr = CALLADDR.TRADE_DETAIL_PARA
    
    #realtobuyList = realtobuyList[:-1]
    if(len(realtobuyList) == 0):
        print "Nothing to buy"
        return
    #return
    for tobuy in realtobuyList:
        
        writeMem(proc, addr, c_uint(tobuy.id))
        
        writeMem(proc, addr + 4, c_ushort(tobuy.slot))
        
        writeMem(proc, addr + 6, c_ushort(tobuy.times))
        writeMem(proc, addr + 8, c_uint(tobuy.price))
        addr += 0xC

        
    addr = CALLADDR.TRADE_HEAD_PARA
    writeMem(proc, addr, c_uint(0x9F488C))
    writeMem(proc, addr + 4, c_uint(0xAFD3A8))
    print "count = %d" % (len(realtobuyList))
    writeMem(proc, addr + 8, c_uint(len(realtobuyList)))
    
    cpara = (c_ubyte * PARASIZE)()
    ip = cast(cpara, POINTER(c_uint))
    ip[0] = addr
    ip[1] = bossid
    ip[2] = 0x4c
    ip[3] = 0
    ip[4] = 0
    ip[5] = 0
    
    paraBuf = writePara(proc, cpara)
    cmdBuf = writeCmd(proc, area.buyCmd)
    
    dowhile(isNormal, [proc])
    execCmd(proc, cmdBuf, paraBuf)

def __testDialog(proc):
    xd_trade = 25166277
    bossid = xd_trade
    sell(proc, bossid)

def sell(proc, bossid):
    
    bossid = int(bossid)
    __openDialog(proc, bossid, 0x4d)
    
    addr = getInt(proc, CALLADDR.DIALOG)
    
    while(addr == 0):
        print 'wait...'
        time.sleep(0.5)
        addr = getInt(proc, CALLADDR.DIALOG)
    
    count = getInt(proc, addr + 0x628)
    print "sell good count = %d" % (count)
    return
    base = getInt(proc, addr + 0x628 + 0xC)
    base += 8
    
    infoList = []
    
    for i in range(count):
        addr = getInt(proc, base)
        print "addr = %x" % (addr)
        infobase = addr + 0x8
        seq = getInt(proc, infobase)
        gid = getInt(proc, infobase + 0xC)
        num = getShort(proc, infobase + 0xC + 0x8)
        price = getInt(proc, infobase + 0xC + 0xC)
        cost = getFloat(proc, infobase + 0xC + 0x14)
        print "seq = %x, gid = %x, num = %d, price = %d, cost = %.3f" % (seq, gid, num, price, cost)
        base += 0xC
        
        info = SellInfo()
        info.seq = seq
        info.id = gid
        info.num = num
        info.price = price
        info.cost = cost
        infoList.append(info)
        
    addr = CALLADDR.TRADE_DETAIL_PARA
    for i in range(count):
        info = infoList[i]
        writeMem(proc, addr, c_int(info.seq))
        writeMem(proc, addr + 4, c_int(0))
        writeMem(proc, addr + 8, c_int(0))
        writeMem(proc, addr + 0xC, c_int(info.num))
        writeMem(proc, addr + 0x10, c_int(info.price))
        addr += 0x14
    
    addr = CALLADDR.TRADE_HEAD_PARA
    writeMem(proc, addr, c_uint(0x9F489C))
    writeMem(proc, addr + 4, c_uint(0xAFD3A8))
    writeMem(proc, addr + 8, c_uint(count))
    
    cpara = (c_ubyte * PARASIZE)()
    ip = cast(cpara, POINTER(c_uint))
    ip[0] = addr
    ip[1] = bossid
    ip[2] = 0x4d
    ip[3] = 0
    ip[4] = 0
    ip[5] = 0
    
    paraBuf = writePara(proc, cpara)
    cmdBuf = writeCmd(proc, area.sellCmd)
    
    dowhile(isNormal, [proc])
    execCmd(proc, cmdBuf, paraBuf)
    
        
def getTradeInfo(proc, bossid):
    
    bossid = int(bossid)
    __openDialog(proc, bossid, 0x4E)
    
    addr = getInt(proc, CALLADDR.DIALOG)
    while(addr == 0):
        print 'Wait...'
        time.sleep(0.5)
        addr = getInt(proc, CALLADDR.DIALOG)
    
    addr = CALLADDR.DIALOG
    #print "%x" % (addr)
    baseaddr = getInt(proc, addr)
    lcount = getInt(proc, baseaddr + 0x5e8)
    rcount = getInt(proc, baseaddr + 0x5fc)
    print "left = %d, right = %d" % (lcount, rcount)
    
    
    
    addr = getInt(proc, baseaddr + 0x5e4)
    
    for count, off in [(lcount, 0x5e4), (rcount, 0x5f8)]:
        addr = getInt(proc, baseaddr + off)
        for i in range(count):
            offset = i * 0x18
            #print "%x" % (addr+offset)
            
            goodid = getInt(proc, addr + offset)
            price = getShort(proc, addr + offset + 0x8)
            trend = getShort(proc, addr + offset + 0x10)
            percent = getShort(proc, addr + offset + 0x12)
            print "goodid = %x, price = %d, trend = %x, percent = %d" % (goodid, price, trend, percent)
        print
    
 
    