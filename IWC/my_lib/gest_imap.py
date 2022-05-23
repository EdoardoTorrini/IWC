from .my_imap import MyIMAP


class ImapStack:

    def __init__(self):
        self.dUsers = {}

    def push(self, sToken, sEmail, sPwd):

        if not sToken in list( self.dUsers.keys() ):
            mThreadImap = MyIMAP(sEmail, sPwd, sToken)
            mThreadImap.start()

            self.dUsers[sToken] = mThreadImap

        else:
            mThreadImap = self.dUsers.get(sToken)

        return mThreadImap

    def pop(self, sToken):

        if sToken in list( self.dUsers.keys() ):
            mThreadImap = self.dUsers.get(sToken)
            mThreadImap.stop()
            self.dUsers.pop(sToken)

    def get(self, sKey):

        for key, val in self.dUsers.items():
            if key == sKey:
                return val

    def clear(self):

        for key, val in self.dUsers.items():
            if isinstance(val, MyIMAP):
                val.stop()

        self.dUsers = {}

    def get_keys(self):
        return list( self.dUsers.keys() )
