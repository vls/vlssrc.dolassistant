# -*- coding: utf-8 -*-

import dolCall, dolScript
import math, time

def distance(x1, y1, x2, y2):
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

def turnPos(proc, x1, y1, e = 5):
    x1 = int(x1)
    y1 = int(y1)
    x,y = dolScript.getSeaPos(proc)
    alpha = dolScript.getAngle(proc)
    
    if(math.fabs(x1 - x) > 8192):
        if(x > x1):
            x = x-16384
        else:
            x = 16384 - x
            
    dis = distance(x1, y1, x, y)
    
    cosa = (x1 - x) / float(dis)
    
    sina = (y1 - y) / float(dis)
    #print 'x = %.3f, x1 = %.3f' % (x, x1)
    #print 'y = %.3f, y1 = %.3f' % (y, y1)
    #print 'alpha = %.3f' % (alpha)
    
    #print "cos = %.3f" % (cosa)
    #print "sin = %.3f" % (sina)
    
    a1 = math.acos(cosa) * 180 / math.pi
    #print a1
    if(sina > 0):
        a1 = 360 - a1
    #print a1
        
    l = math.fabs(a1 - alpha)
    print "degree diff = %.3f" % (l)
    
    if (l > e):
        if(l > 30):
            dolCall.sail(proc, 1)
            time.sleep(1)
        print "Turn to %.3f" % (a1)
        dolCall.turn(proc, a1)
        if(l > 30):
            time.sleep(1)
            dolCall.sail(proc, 4)

