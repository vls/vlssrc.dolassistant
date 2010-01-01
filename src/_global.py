class MyList(list):
    def __str__(self):
        str = ''
        for x in self:
            str += x
            str += ', '
        return '[%s]' % (str[:-2])