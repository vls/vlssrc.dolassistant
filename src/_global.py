class MyList(list):
    def __str__(self):
        str = ''
        for x in self:
            str += x
            str += ', '
        return '[%s]' % (str[:-2])
    
    
MOD_ALT = 1
MOD_CTRL = 2
MOD_SHIFT = 4
MOD_WIN = 8