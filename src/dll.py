import sys
sys.path.append("I:\document\My Documents\Visual Studio 2008\Projects\Cpp\pyqmacro\Debug")
import pyqmacro




def Key(funcname, hwnd, key):
    pyqmacro.invoke('BGKM5.dll', funcname, [hwnd, key])

def Mouse(funcname, hwnd, x, y):
    pyqmacro.invoke('BGKM5.dll', funcname, [hwnd, x, y])
    
def BGKM5(funcname, hwnd, args):
    pyqmacro.invoke('BGKM5.dll', funcname, args.insert(0,hwnd))
    
    
if __name__ == "__main__":
    pyqmacro.dllHelp('BGKM5.dll')





