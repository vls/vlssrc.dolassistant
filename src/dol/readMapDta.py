# -*- coding: utf-8 -*-
from rtBase import rtBaseClass, rtCityBase
import readMap
import dolCallEnum

class readMapCityBase(rtCityBase):
    def __init__(self):
        rtCityBase.__init__(self)
        self.libName = '書庫'
        self.downShip = 0
        self.libEnterPos = (0, 0)
        self.libEnterID = 0
        self.libOutID = 0
        self.manID = 0
        self.toReadPos = (0, 0)
    
    def getDockName(self):
        return self.name + '碼頭'


class sw(readMapCityBase):
    '''
    塞维尔
    '''
    cityID = 0x4020008
    def __init__(self):
        readMapCityBase.__init__(self)
        self.name = '塞維爾'
        
        self.cityRouteDict = {
                              fl.cityID : [(15814, 3268)]
                              }
        self.downShip = dolCallEnum.MoveTo.Plaza
        self.libEnterID = 0x80100a8
        self.libEnterPos = (46955, 35208)
        
        self.libOutID = 0xc0108ee
        self.manID = 0x1800599
        self.toReadPos = (2540, 4630)

class london(readMapCityBase):
    '''
    倫敦
    '''
    cityID = 0x41d003b
    def __init__(self):
        readMapCityBase.__init__(self)
        self.name = '倫敦'
        self.cityRouteDict = {
                              duofo.cityID : [(16334, 2473)]
                              }
        self.downShip = dolCallEnum.MoveTo.Plaza
        self.libEnterID = 0x806002d
        self.libEnterPos = (48347, 20175)
        self.libOutID = 0xc0607da
        self.manID = 0x18004f7
        self.toReadPos = (2174, 4365)

class fl(readMapCityBase):
    '''
    法魯
    '''
    cityID = 0x401000c
    def __init__(self):
        readMapCityBase.__init__(self)
        self.name = '法魯'
        self.cityRouteDict = {
                              sw.cityID : [(15819, 3273), (15896,3267)]
                              }

class duofo(readMapCityBase):
    '''
    多佛
    '''
    cityID = 0x41d0020
    def __init__(self):
        readMapCityBase.__init__(self)
        self.name = '多佛'
        self.cityRouteDict = {
                              london.cityID : [(16341, 2491), (16328, 2424)]
                              }