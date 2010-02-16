# -*- coding: utf-8 -*-


class kaituDtaBase():
    def __init__(self):
        self.churchEnterID = 0
        self.churchOutID = 0
        self.churchOutPos = (0, 0)
        self.churchPos = (0, 0)
        self.reportEnterID = 0
        self.reportOutID = 0
        self.reportNPCID = 0
        self.reportEnterPos = (0, 0)
        self.reportPos = (0, 0)
        self.kaiPos = (0, 0)
        self.subSeq = 0
        self.seq = 0

class art(kaituDtaBase):
    '''
    美术
    '''
    def __init__(self):
        kaituDtaBase.__init__(self)
        self.subSeq = 2

class reMei1(art):
    '''
    热那亚美1
    '''
    def __init__(self):
        art.__init__(self)
        self.churchOutID = 0xc1812a1
        self.churchOutPos = (5015, 9629)
        self.churchEnterID = 0x8180035
        self.churchPos = (41205, 22233)
        self.reportEnterID = 0x8180017
        self.reportOutID = 0xc18063d
        self.reportNPCID = 0x180045f
        self.reportPos = (2568, 4206)
        self.reportEnterPos = (38306, 18914)
        self.kaiPos = (4798, 6316)

class reMei2(reMei1):
    '''
    热那亚美2
    '''
    def __init__(self):
        reMei1.__init__(self)
        self.kaiPos = (4515, 7632)
        
class reMei3(reMei1):
    '''
    熱那亞美3
    '''
    def __init__(self):
        reMei1.__init__(self)
        self.kaiPos = (4469, 8777)
        
class mei5(art):
    '''
    倫敦美5
    '''
    def __init__(self):
        art.__init__(self)
        self.churchOutID = 0xc0e023b
        self.churchOutPos = (4997, 9563)
        self.churchPos = (17376, 12780)
        self.churchEnterID = 0x80e00da
        self.reportEnterPos = (17524, 16325)
        self.reportEnterID = 0x80e00dd
        self.reportPos = (2596, 4433)
        self.reportNPCID = 0x1800476
        self.reportOutID = 0xc0e010b
        self.kaiPos = (5863, 6999)