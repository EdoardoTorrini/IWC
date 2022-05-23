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

            while 1:

                # bisogna poter cambiare cartella
                status, messages = self.oImap.select("INBOX")
                nMess = int(messages[0].decode("utf-8"))

                for i in range(1, nMess + 1):
                    res, msg = self.oImap.fetch(str(i), "(RFC822)")

                    for response in msg:
                        if isinstance(response, tuple):
                            msg = email.message_from_bytes(response[1])

                            sIdMess = msg["Message-ID"]
                            if sIdMess not in self.dMailDict.keys():
                                self.dMailDict[sIdMess] = msg

        except Exception as sErr:
            print(self.email, "-", sErr)

    def getMailDict(self):
        return self.dMailDict

    def getMailBoxes(self):
        return self.aBoxList

    def getElementFromIdMess(self, sReqIdMess):

        for mail in self.dMailDict.keys():
            if mail == sReqIdMess:
                return self.dMailDict[mail]

    def readMessageFromId(self, sReqIdMess):

        oMsg = self.dMailDict.get(sReqIdMess)
        if oMsg is not None:
            if oMsg.is_multipart():
                return oMsg.get_payload(0)
            else:
                return oMsg.get_payload(None, True)
