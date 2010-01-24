from dolCall import *
from dolScript import *


def dowhile(callable, args = [], interval = 0.2):
    while(not callable(*args)):
        time.sleep(interval)

def custom_safe(proc, num):
    dowhile(isNormal, [proc])
    custom(proc, num)
    
        

def testfunc(s1, s2):
    print s1
    print s2
    return False

def main():
    dowhile(testfunc, ['begin', 'end'])
    
        
if __name__ == "__main__":
    main()