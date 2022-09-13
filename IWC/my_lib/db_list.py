from django.db import models


class SeparateValueField(models.TextField):
    
    def __init__(self, *arg, **kargs):
        super(SeparateValueField, self).__init__(*arg, **kargs)

        self.aVal = []

    def append(self, value):
        self.aVal.append(value)

    def __str__(self):
        sRet = ""
        for elem in self.aVal:
            sRet += "{};".format(elem)

        return sRet

    def __getitem__(self, key):
        if isinstance(key, slice):
            index = range(*key.indices(len(self.aVal)))
            return [self.aVal[i] for i in index]
        return self.aVal[key]

    def __getslice__(self, i, j):
        return self.__getitem__(slice(i, j))
