from datetime import datetime
from email.utils import parsedate
import time


class DateTimeConverter:

    def __init__(self, sDate, sFormat=None, bEmail=False):

        if sFormat is not None:
            self.dObj = datetime.strptime(sDate, sFormat)

        if bEmail is True:
            self.dObj = datetime.fromtimestamp(time.mktime(parsedate(sDate)))

    def getDateFormatted(self, sFormat):
        return self.dObj.strftime(sFormat)
