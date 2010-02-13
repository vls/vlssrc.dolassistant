# -*- coding: utf-8 -*-
from rtBase import rtBaseClass, rtCityBase
import readMap
import dolCallEnum

class readMapCityBase(rtCityBase):
    def __init__(self):
        rtCityBase.__init__(self)
        self.dockName = ''
        self.libName = ''
        self.downShip = 0
        self.libEnterPos = (0, 0)
        self.libEnterID = 0
        self.libOutID = 0
        self.manID = 0
        self.toReadPos = (0, 0)

def getCityID(city):
    assert isinstance(city, readMapCityBase)
    return city.cityID

class sw(readMapCityBase):
    '''
    塞维尔
    '''
    cityID = 0x4020008
    def __init__(self):
        self.name = '塞維爾'
        
        self.cityRouteDict = {
                              fl.cityID : [(15814, 3268)]
                              }
        self.dockName = self.name + '碼頭'
        self.downShip = dolCallEnum.MoveTo.Plaza
        self.libEnterID = 0x80100a8
        self.libEnterPos = (46955, 35208)
        self.libName = '書庫'
        self.libOutID = 0xc0108ee
        self.manID = 0x1800599
        self.toReadPos = (2540, 4630)

class fl(readMapCityBase):
    '''
    法魯
    '''
    cityID = 0x401000c
    def __init__(self):
        self.name = '法魯'
        self.dockName = self.name + '碼頭'
        self.cityRouteDict = {
                              sw.cityID : [(15819, 3273), (15896,3267)]
                              }
        