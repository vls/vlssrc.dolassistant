# -*- coding: utf-8 -*-
from dolCall import *
from dolScript import *
from dolCallEnum import *

def dowhile(callable, args = [], interval = 0.2):
    while(not callable(*args)):
        time.sleep(interval)

def custom_safe(proc, num):
    dowhile(isNormal, [proc])
    custom(proc, num)
    
def follow_safe(proc, userid):
    type = getLocationType(proc)
    if(type == LocType.City or type == LocType.House):
        follow(proc, userid)
    elif(type == LocType.Sea):
        seafollow(proc, userid)
    else:
        print "未处理的地方类型"
        

def testfunc(s1, s2):
    print s1
    print s2
    return False

def main():
    dowhile(testfunc, ['begin', 'end'])
    
        
if __name__ == "__main__":
    main()