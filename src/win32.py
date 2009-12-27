import win32process
import win32gui
import win32con
import win32api
from ctypes import *
 
kernel32 = windll.LoadLibrary("kernel32.dll") 
ReadProcessMemory = kernel32.ReadProcessMemory 
WriteProcessMemory = kernel32.WriteProcessMemory 
OpenProcess = kernel32.OpenProcess 