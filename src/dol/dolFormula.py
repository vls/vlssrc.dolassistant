# -*- coding: utf-8 -*-


def getBasic(lv, num, profit):
    total = profit * num
    basic = (total + lv + 1) / float(lv + 1) // 100
    if(total > 100000):
        basic *= 4
    elif(total > 10000):
        basic *= 2
    
    return basic

def getSpecial(lv, num, dis):
    spe = num * dis * 50 // float(lv + 50)
    if (spe > 500):
        spe = 500
    
    return spe

def getSpeExp(lv, num, profit, dis):    
    return getBasic(lv, num, profit) + getSpecial(lv, num, dis)

def getMaxEff(lv, profit, dis):
    
    maxnum = 1
    maxexp = getSpeExp(lv, 1, profit, dis)
    maxeff = maxexp
    for num in range(2, 100):
        exp = getSpeExp(lv, num, profit, dis)
        eff = exp / num
        if(eff > maxeff):
            maxeff = eff
            maxnum = num
            maxexp = exp
            
    return (maxnum, maxeff, maxexp)
    



def main():
    lv = 17
    dis = 12
    num = 20
    profit = 884 - 143
    maxeff = getMaxEff(lv, profit, dis)
    print maxeff

if __name__ == "__main__":
    main()