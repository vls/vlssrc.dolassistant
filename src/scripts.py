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
    """��ȡ��ǰ���������д󺽺��Ľ�ɫ��
    """
    nameList = []
    procHelper = helper.WindowHelper()
    dolProcList = procHelper.getProcListByClassName(dolScript.dolClassName)
    for proc in dolProcList:
        nameList.append(dolScript.getRoleName(proc))
        
    return nameList