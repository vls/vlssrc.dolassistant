# -*- coding: gbk -*-
import win32
import helper
from ctypes import *

dolClassName = "Greate Voyages Online Game MainFrame"

class addr:
    # 台服C5+
    HP = 0xB6FAF0
    ROLENAME = HP - 0xD8 #角色名基址
#===============================================================================
# address = 0x4ffc7e
#    # address = 0x0040103c                                
#    buffer = ctypes.c_char_p('__')
#    bytesRead = ctypes.c_ulong(0)
#    bufferSize =  len(buffer.value)
# 
#    # clearly that byref means "by reference", i.e., "&" in C. so smart~
#    ReadProcessMemory(procHandle.handle, address, buffer, bufferSize, ctypes.byref(bytesRead))
#    print buffer._objects
#    print bytesRead
# 
#    buffer = ctypes.c_char_p('0xdd0xdd')
#    bytesWrite = ctypes.c_ulong(0)
#    bufferSize =  len(buffer.value)
#===============================================================================


    
def getRoleName(proc):
    
    buf = c_int(0)
    bytesRead = c_ulong(0)
    bufferSize = 4
    win32.ReadProcessMemory(proc.handle, addr.ROLENAME, byref(buf), bufferSize, byref(bytesRead))

    address = buf.value
    lenAddress = buf.value - 12 #名字长度的地址（中文字数目）


    
    win32.ReadProcessMemory(proc.handle, lenAddress, byref(buf), bufferSize, byref(bytesRead))
    
    nameLength = buf.value * 2

    
    buf = c_wchar_p(' ' * nameLength)
    bufferSize = nameLength
    
    win32.ReadProcessMemory(proc.handle, address, buf, bufferSize, byref(bytesRead))

    return buf.value
    
    #ReadProcessMemory(procHandle.handle, address, buffer, bufferSize, ctypes.byref(bytesRead))

def getHP(proc):
    buf = c_int(0)
    bytesRead = c_ulong(0)
    bufferSize = 4
    win32.ReadProcessMemory(proc.handle, addr.HP, byref(buf), bufferSize, byref(bytesRead))
    return buf.value
    
    
   
                            
    
    
if __name__ == "__main__":
     procHelper = helper.WindowHelper()
     dolProcList = procHelper.getProcListByClassName(dolClassName)
     proc = dolProcList[0]
     print getRoleName(proc)
     
    