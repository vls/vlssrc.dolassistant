# -*- coding: utf-8 -*-


class MoveTo:
    Plaza = 0x8f # 广场
    Biz = 0x90 #商业
    BizHouse = 0x91 #商务会馆
    DockPlaza = 0x8e #码头广场
    Dock = 0x42 #进入码头
    Palace = 0x7a #进入皇宫
    Land = 0x92 #陆地
    
class LocType:
    Sea = 0x4 #海洋
    City = 0x8 #城市
    House = 0xc # 室内
    Dock = 0x1c # 码头
    LandDock = 0x20 # 登陆点
    Land = 0x10
    Land2 = 0x13
    

buyCountDict = {
            0:1,
            1:2,
            2:5,
            3:10,
            4:20,
            5:50}



class SellInfo():
    def __init__(self):
        self.seq = 0
        self.id = 0
        self.num = 0
        self.price = 0
        self.cost = 0.0
    
    def __repr__(self):
        return "(id = %x, num = %d, price = %d, cost = %d, profit = %d)\n" % (self.id, self.num, self.price, self.cost, self.price - self.cost)
        
class BuyInfo():
    def __init__(self):
        self.id = 0
        self.name = ""
        self.remain = 0
        self.info = None
        
class ToBuy():
    def __init__(self):
        self.id = 0
        self.slot = 0
        self.times = 0
        self.price = 0
        
    def getRealNum(self):
        return buyCountDict[self.slot - 0xA300] * self.times
    
    def __repr__(self):
        realslot = self.slot - 0xA300 
        return "(ID = %x, slot = %d(%d), times = %d, price = %d)\n" % (self.id, realslot, buyCountDict[realslot],  self.times, self.price)