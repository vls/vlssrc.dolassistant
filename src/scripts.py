# -*- coding: gbk -*-
from dol import dolScript
import w32
import helper


def test(st,st2):
    print 'Test OK!!! String = %s / %s' % (st,st2)
    return None

def test2():
    print 'Test2 OK!!!'
    
    
def getRoleNameList():
    """获取当前机器的所有大航海的角色名
    """
    nameList = []
    procHelper = helper.WindowHelper()
    dolProcList = procHelper.getProcListByClassName(dolScript.dolClassName)
    for proc in dolProcList:
        nameList.append(dolScript.getRoleName(proc))
        
    return nameList