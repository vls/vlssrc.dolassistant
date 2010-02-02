# -*- coding: utf-8 -*-

FIRM_NAME_ADDR = 0xb7139c
FIRM_BASE_ADDR = 0xbe4738

GOOD_NAME_ADDR = 0xb7051c

from global_ import *
from dll import Mouse, Key
from helper import ProcessHelper
import dolCallAddr

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
        print "%d" % (getByte(proc, addr + 0x6ac))
        print "%d" % (getByte(proc, addr + 0x5e4))

class FirmHelper:
    
    def __init__(self, proc):
        self.nameDict = {}
        self.currentFirmSeq = -1
        self.firmNameList = self.getFirmNameList(proc)

    def getFirmNameList(self, proc):
        '''
        获取商会名称列表
        '''
        nameList = []
        addr = getInt(proc, FIRM_NAME_ADDR)
        while(addr > 0):
            key = getInt(proc, addr + 12)
            nameaddr = getInt(proc, addr + 0x30)
            name = getStringW(proc, nameaddr, 40)
            print "key = %x, name = %s" % (key,name)
            nameList.append(name)
            addr = getInt(proc, addr)
        
        return nameList
            
    
    
    
    def getFirmID(self, proc):
        '''
        获取当前商会ID
        '''
        addr = getInt(proc, FIRM_BASE_ADDR)
        fid = getShort(proc, addr + 0x5e0)
        #print fid
        return fid
    
    def getGoodsNameList(self, proc):
        
        nameList = []
        firmID = self.getFirmID(proc)
        for i in range(150):
            pass
    
    def getGoodName(self, proc, gid):
        '''
        获取物品名称
        '''
        if(self.nameDict.has_key(gid)):
            return self.nameDict[gid]
        
        A = getInt(proc, GOOD_NAME_ADDR + 4)
        B = getInt(proc, GOOD_NAME_ADDR + 8)
        groupid = gid // 16
        newaddr = A + (groupid % B) * 4
        
        #print "newaddr = %x" % (newaddr)
        
        addr = getInt(proc, newaddr)
            
        while(addr != 0):
            tempgroupid = getInt(proc, addr + 12)
            #print "tempgroupid = %x" % (tempgroupid)
            tempgid = getInt(proc, addr)
            #print "tempgid = %x" % (tempgid)
            if(tempgroupid == groupid and tempgid == gid):
                break
            
            addr = getInt(proc, addr + 8)
        
        if(addr != 0):
            addr = getInt(proc, addr + 4)
            addr = getInt(proc, addr + 12)
            name = getStringW(proc, addr, 40)
            
            self.nameDict[gid] = name
            
            return name
        
        return None
    
    def getGoodsInfo(self, proc):
        '''
        获取物品信息
        '''
        infoList = []
        addr = getInt(proc, FIRM_BASE_ADDR + 4)
        baseaddr = getInt(proc, addr + 200)
        
        for i in range(150):
            addr = getInt(proc, baseaddr + 8)
            addr = getInt(proc, addr + 12)
            gid = getInt(proc, addr + 12)
                    
            name = self.getGoodName(proc, gid)
            if(name == None):
                break
            
            price = getInt(proc, addr + 12 + 12)
            count = getInt(proc, addr + 12 + 12 + 0x10)
            print "good id = %x, name = %s, price = %d, count = %d" % (gid, name, price, count)
            
            info = GoodInfo()
            info.id = gid
            info.name = name
            info.price = price
            info.count = count
            info.firmSeq = self.currentFirmSeq
            info.firmName = self.firmNameList[info.firmSeq]
            
            
            infoList.append(info)
            
            baseaddr = getInt(proc, baseaddr)
            
        return infoList
    
    def searchGoods(self, proc):
        helper = ProcessHelper()
        hwnd = helper.getHwndByProc(proc)
        
        nameList = self.getFirmNameList(proc)
        
        addr = getInt(proc, FIRM_BASE_ADDR)
        if(addr > 0):
            rank = getByte(proc, addr + 0x5e4)
            
            nowrank = rank
            if(nowrank == rank):
                while(nowrank == rank and nowrank < 250):
                    print "-----------search [%s]-------------" % (nameList[rank])
                    self.currentFirmSeq = nowrank
                    
                    
                    num4 = getInt(proc, FIRM_BASE_ADDR) # 当前窗口为商会一览 或者 商会店铺， 这个值会不同
                    Mouse('LClick', hwnd, 0x248, 0x179) #点击"商会店铺"按钮
                    time.sleep(2)
                    num5 = getInt(proc, FIRM_BASE_ADDR + 4)
                    
                    waitCount = 0
                    while(num4 == getInt(proc, FIRM_BASE_ADDR) or num5 == 0):
                        time.sleep(0.5)
                        num5 = getInt(proc, FIRM_BASE_ADDR + 4)
                        if (waitCount > 15):
                            break
                        waitCount += 1
                    
                    
                    
                    if(waitCount < 10 or num4 != getInt(proc, FIRM_BASE_ADDR)):
                        #readinfo
                        self.getGoodsInfo(proc)
                        
                        num4 = getInt(proc, FIRM_BASE_ADDR)
                        Key('KeyClick', hwnd, 0x1b) #ESC
                        
                        waitCount = 0
                        while(num4 == getInt(proc, FIRM_BASE_ADDR)):
                            time.sleep(0.5)
                            waitCount += 1
                        
                    Key('KeyClick', hwnd, 40) #down arrow
                    time.sleep(0.5)
                    
                    while(getByte(proc, addr + 0x6ac) != rank + 1):
                        
                        time.sleep(0.5)
                    
                    rank = getByte(proc, addr + 0x5e4)     
                        
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