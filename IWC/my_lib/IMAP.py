from threading import Thread
import imaplib
import email


class MyIMAP(Thread):

    def __init__(self, sEmail, sPwd, sToken):
        super().__init__(daemon=True)

        self.id = sToken
        self.email = sEmail
        self.pwd = sPwd
        self.bRun = False

        self.aBoxList = []
        self.dMailDict = {}

        self.recv = None
        self.sSelBoxMail = '"INBOX"'

        # TODO: se non è connesso a internet va in errore
        self.oImap = imaplib.IMAP4_SSL("imap.gmail.com")

    def check_account(self):

        try:
            self.recv = self.oImap.login(self.email, self.pwd)
            self.oImap.logout()
            return {1: "OK"}
        except Exception as sVal:
            return {0: sVal}

    def run(self):
        self.bRun = True

        try:
            self.recv = self.oImap.login(self.email, self.pwd)
            self.aBoxList = [ box.decode("utf-8") for box in self.oImap.list()[1] ]

            for box in self.getMailBoxes().keys():
                if box not in self.dMailDict.keys():
                    self.dMailDict[box] = {}

            while 1:

                # bisogna poter cambiare cartella
                for box in self.getMailBoxes().keys():
                    status, messages = self.oImap.select(box)
                    nMess = int(messages[0].decode("utf-8"))

                    for i in range(1, nMess + 1):
                        res, msg = self.oImap.fetch(str(i), "(RFC822)")

                        for response in msg:
                            if isinstance(response, tuple):
                                msg = email.message_from_bytes(response[1])
                                aFile = []

                                sIdMess = msg["Message-ID"]
                                if sIdMess not in self.dMailDict[box].keys():
                                    self.dMailDict[box][sIdMess] = msg
                                    for part in msg.walk():
                                        if part.get_filename() is not None:
                                            aFile.append(part.get_filename())
                                        self.dMailDict[box][sIdMess]["File"] = aFile

        except Exception as sErr:
            print(self.email, "-", sErr)

    def getMailDict(self):
        if self.sSelBoxMail in self.dMailDict.keys():
            return self.dMailDict[self.sSelBoxMail]
        return {}

    def getMailBoxes(self):
        dBoxes = {}
        for elem in self.aBoxList:
            nFind = elem.find("/\" ")
            sKey = elem[nFind + len("/\" "):]
            if sKey.find("Gmail]") > -1:
                if sKey.find("/") > -1:
                    dBoxes[sKey] = sKey[sKey.find("/")+1:-1]
            else:
                dBoxes[sKey] = sKey[1:-1]
        return dBoxes

    def setBoxMail(self, sIdBox):
        if sIdBox in self.getMailBoxes().keys():
            setattr(self, "sSelBoxMail", sIdBox)

    def getElementFromIdMess(self, sReqIdMess):

        for mail in self.dMailDict[self.sSelBoxMail].keys():
            if mail == sReqIdMess:
                return self.dMailDict[self.sSelBoxMail][mail]

    def readMessageFromId(self, sReqIdMess):

        oMsg = self.dMailDict[self.sSelBoxMail].get(sReqIdMess)
        if oMsg is not None:
            if oMsg.is_multipart():
                return oMsg.get_payload(0)
            else:
                return oMsg.get_payload(None, True)

    def getCurrentBoxMail(self):
        return self.sSelBoxMail
