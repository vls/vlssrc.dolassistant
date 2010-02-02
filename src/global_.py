import sys


class MyList(list):
    def __str__(self):
        str = ''
        for x in self:
            str += x
            str += ', '
        return '[%s]' % (str[:-2])


def __reloadMod(modstr):
        if sys.modules.has_key(modstr):
            module = sys.modules[modstr]
            reload(module)
        else:
            module = __import__(modstr)
        
        return module    
    
MOD_ALT = 1
MOD_CTRL = 2
MOD_SHIFT = 4
MOD_WIN = 8