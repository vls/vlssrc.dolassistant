# -*- coding: utf-8 -*-

FIRM_NAME_ADDR = 0xb7139c
FIRM_BASE_ADDR = 0xbe4738 # 跟CALLADDR.DIALOG一样的值

GOOD_NAME_ADDR = 0xb7051c

from global_ import *
from dll import Mouse, Key
from helper import ProcessHelper
import dolCallAddr, dolAddr
import dolCall, dolScript
from global_ import dowhile
import csv
ADDR = dolAddr.ADDR

CALLADDR = dolCallAddr.TW

class GoodInfo:
    def __init__(self):
        self.id = 0
        self.name = ""
        self.price = 0
        self.count = 0
        self.firmSeq = 0
        self.firmName = ""

def __test(proc):
        addr =  getInt(proc, FIRM_BASE_ADDR)
        print "%x" % (addr)
        print "%x" % (getInt(proc, FIRM_BASE_ADDR + 4) )
        print "%x" % (getInt(proc, CALLADDR.DIALOG))
        print "%x" % (getInt(proc, CALLADDR.DIALOG + 4))

def __testOpen(proc, dia):
    dia = int(dia)
    
    
    bossid = dolScript.getTabId(proc)
    if(bossid != 0):
        print dolScript.getTabName(proc)
        
        dolCall.openDialog(proc, bossid, dia, False)
        time.sleep(2)
        addr = getInt(proc, CALLADDR.DIALOG)
        
    else:
        print 'no tab'
        
def __testsearch(proc):
    helper = FirmHelper(proc)
    helper.searchGoods()

def waitLoad(proc):
    #num4 = getInt(proc, FIRM_BASE_ADDR) # 当前窗口为商会一览 或者 商会店铺， 这个值会不同
    num5 = getInt(proc, FIRM_BASE_ADDR + 4)
    
    if(num5 == 0):
        print 'wait...'
        return False
    
    return True


def __getname(proc):
    '''
        获取物品名称
    '''
    gid = 0x16f6eb
    addr = 0xB70680
    
    #gid = 0x186aea
    #addr = GOOD_NAME_ADDR + 4
    
    A = getInt(proc, addr)
    B = getInt(proc, addr + 4)
    groupid = gid // 16
    print "%x" % (groupid)
    print "A = %x" % (A)
    print "%%b = %x" % (groupid % B)
    print "* 4 = %x " % (groupid % B *4) 
    
    newaddr = A + (groupid % B) * 4
    
    print "newaddr = %x" % (newaddr)
    
    addr = getInt(proc, newaddr)
    print "addr = %x" % (addr)
    
    
    while(addr != 0):
        tempgroupid = getInt(proc, addr + 12)
        print "tempgroupid = %x" % (tempgroupid)
        tempgid = getInt(proc, addr)
        print "tempgid = %x" % (tempgid)
        if(tempgroupid == groupid and tempgid == gid):
            break
        
        addr = getInt(proc, addr + 8)
        print "addr = %x" % (addr)
        
    
    if(addr != 0):
        addr = getInt(proc, addr + 4)
        addr = getInt(proc, addr + 12)
        name = getStringW(proc, addr, 40)
        

        print name
        return name
    
    return None

def __name2(proc):
    addr = 0x4D8338C
    temp = addr
    id = getInt(proc, addr)
    addr = getInt(proc, addr + 4)
    addr = getInt(proc, addr + 12)
    name = getStringW(proc, addr, 40)
    
    if (len(name) != 0 and len(name) != 40):
        
        print "[%x] %#x = %s" % (temp, id, name)

def __name(proc):
    for addr in range(0x4EEAFFC-0x3FF0, 0x4EEAFFC+ 0x5FFF0, 0x10):
        temp = addr
        id = getInt(proc, addr)
        addr = getInt(proc, addr + 4)
        addr = getInt(proc, addr + 12)
        name = getStringW(proc, addr, 40)
        
        if (len(name) != 0 and len(name) != 40):
            print "[%x] %#x = %s" % (temp, id, name)
            

class abstractwriter():
    def __init__(self):
        pass
    def write(self, *msg):
        pass
    
class csvWriter(abstractwriter):
    def __init__(self, filepath):
        abstractwriter.__init__(self)
        self.filepath = filepath
        with open(self.filepath, "w"):
            pass
        self.handle = open(self.filepath, "a")
        self.writer = csv.writer(self.handle, lineterminator = '\n')
    
    def __del__(self):
        self.handle.close()
        
    def write(self, *msg):
        msgList = []
        for m in msg:
            if(isinstance(m, unicode)):
                msgList.append(m.encode('gbk'))
            else:
                msgList.append(m)
        self.writer.writerows([msgList])
        
    

FILEPATH = 'firmgoods.csv'        
        
class FirmHelper:
    
    def __init__(self, proc):
        self.nameDict = {}
        self.currentFirmSeq = -1
        self.proc = proc
        self.firmNameList = self.getFirmNameList()
        
        self.writer = csvWriter(FILEPATH) 

    def getFirmNameList(self):
        '''
        获取商会名称列表
        '''
        nameList = []
        addr = getInt(self.proc, FIRM_NAME_ADDR)
        while(addr > 0):
            key = getInt(self.proc, addr + 12)
            nameaddr = getInt(self.proc, addr + 0x30)
            name = getStringW(self.proc, nameaddr, 40)
            #print "key = %x, name = %s" % (key,name)
            nameList.append(name)
            addr = getInt(self.proc, addr)
        
        return nameList
            
    
    
    
    def getFirmID(self):
        '''
        获取当前商会ID
        '''
        addr = getInt(self.proc, FIRM_BASE_ADDR)
        fid = getShort(self.proc, addr + 0x5e0)
        #print fid
        return fid
    
    def getGoodsNameList(self):
        
        nameList = []
        firmID = self.getFirmID()
        for i in range(150):
            pass
    
    def getGoodName(self, gid):
        '''
        获取物品名称
        '''
        if(self.nameDict.has_key(gid)):
            return self.nameDict[gid]
        
        A = getInt(self.proc, GOOD_NAME_ADDR + 4)
        B = getInt(self.proc, GOOD_NAME_ADDR + 8)
        groupid = gid // 16
        newaddr = A + (groupid % B) * 4
        
        #print "newaddr = %x" % (newaddr)
        
        addr = getInt(self.proc, newaddr)
            
        while(addr != 0):
            tempgroupid = getInt(self.proc, addr + 12)
            #print "tempgroupid = %x" % (tempgroupid)
            tempgid = getInt(self.proc, addr)
            #print "tempgid = %x" % (tempgid)
            if(tempgroupid == groupid and tempgid == gid):
                break
            
            addr = getInt(self.proc, addr + 8)
        
        if(addr != 0):
            addr = getInt(self.proc, addr + 4)
            addr = getInt(self.proc, addr + 12)
            name = getStringW(self.proc, addr, 40)
            
            self.nameDict[gid] = name
            
            return name
        
        return None
    
    def getGoodsInfo(self):
        '''
        获取物品信息
        '''
        infoList = []
        addr = getInt(self.proc, FIRM_BASE_ADDR + 4)
        baseaddr = getInt(self.proc, addr + 200)
        
        for i in range(150):
            addr = getInt(self.proc, baseaddr + 8)
            addr = getInt(self.proc, addr + 12)
            gid = getInt(self.proc, addr + 12)
            if(gid == 0):
                break
                    
            name = self.getGoodName(gid)
            
            
            price = getInt(self.proc, addr + 12 + 12)
            count = getInt(self.proc, addr + 12 + 12 + 0x10)
            print "good id = %x, name = %s, price = %d, count = %d" % (gid, name, price, count)
            
            info = GoodInfo()
            info.id = gid
            info.name = name
            info.price = price
            info.count = count
            info.firmSeq = self.currentFirmSeq + 1
            info.firmName = self.firmNameList[self.currentFirmSeq]
            
            
            infoList.append(info)
            
            self.writer.write("%#x" % ( info.id), info.name, info.price, info.count, info.firmName, info.firmSeq)
            
            baseaddr = getInt(self.proc, baseaddr)
            
        return infoList
    
    def searchGoods(self):
        helper = ProcessHelper()
        hwnd = helper.getHwndByProc(self.proc)
        
        
        
        bossid = dolScript.getTabId(self.proc)
        
        if(bossid == 0):
            print "no tab!"
            return
        
        addr = getInt(self.proc, FIRM_BASE_ADDR)
        if(addr == 0):
            dolCall.openDialog(self.proc, bossid, 0x7b)
            
            dowhile(waitLoad, [self.proc])
            addr = getInt(self.proc, FIRM_BASE_ADDR)
            
        print "%x" % (addr)
        if(addr > 0):
            
            rank = getByte(self.proc, addr + 0x5e4)
            nameList = self.getFirmNameList()
            nowrank = rank
            if(nowrank == rank):
                self.writer.write('ID', 'name', 'price', 'count', 'firm', 'firmseq')
                while(nowrank == rank and nowrank < 250):
                    
                    print "-----------search [%s]-------------" % (nameList[rank])
                    self.currentFirmSeq = nowrank
                    
                    
                    num4 = getInt(self.proc, FIRM_BASE_ADDR) # 当前窗口为商会一览 或者 商会店铺， 这个值会不同
                    Mouse('LClick', hwnd, 0x248, 0x179) #点击"商会店铺"按钮
                    time.sleep(2)
                    num5 = getInt(self.proc, FIRM_BASE_ADDR + 4)
                    
                    waitCount = 0
                    while(num4 == getInt(self.proc, FIRM_BASE_ADDR) or num5 == 0):
                        time.sleep(0.5)
                        num5 = getInt(self.proc, FIRM_BASE_ADDR + 4)
                        if (waitCount > 15):
                            break
                        waitCount += 1
                    
                    
                    
                    if(waitCount < 10 or num4 != getInt(self.proc, FIRM_BASE_ADDR)):
                        #readinfo
                        infoList = self.getGoodsInfo()
                        
                        
                        
                        num4 = getInt(self.proc, FIRM_BASE_ADDR)
                        Key('KeyClick', hwnd, 0x1b) #ESC
                        
                        waitCount = 0
                        while(num4 == getInt(self.proc, FIRM_BASE_ADDR)):
                            time.sleep(0.5)
                            waitCount += 1
                        
                    Key('KeyClick', hwnd, 40) #down arrow
                    time.sleep(0.5)
                    
                    while(getByte(self.proc, addr + 0x6ac) != rank + 1):
                        
                        time.sleep(0.5)
                    
                    rank = getByte(self.proc, addr + 0x5e4)     
                        
                    nowrank += 1
                    
                    #print rank
                    #print nowrank
        else:
            print "Dialog Not opened"
    
def main():
    print 'main'

if __name__ == "__main__" and __package__ == None:
    print __package__
    main()