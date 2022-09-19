from threading import Thread
import imaplib

from . import ImapMail
from . import APIMail


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
        self.tIMAP_USER = APIMail(self.id)

        self.oImap = None

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
                        aATT = ["(RFC822)", "(UNSEEN)"]

                        for elem in aATT:
                            match elem:

                                case "(RFC822)":
                                    res, msg = self.oImap.fetch(str(i), elem)
                                    ImapMail(msg, self.id, box).start()

                                case "(UNSEEN)":
                                    try:
                                        res, msg = self.oImap.search(None, elem)

                                        if res == "OK":
                                            if len(msg[0].split()) > 0:
                                                ImapMail(msg, self.id, '"INBOX"').start()

                                    except Exception as sErr:
                                        print("IMAP:", sErr)

                                case _:
                                    print("Qualcosa è andato storto")

                # TODO: proviamo

        except Exception as sErr:
            print(self.email, "-", sErr)

    ''' metodi per il funzionamento della libreria '''

    def setBoxMail(self, sIdBox):
        if sIdBox in self.getMailBoxes().keys():
            setattr(self, "sSelBoxMail", sIdBox)

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

    def getCurrentBoxMail(self):
        return self.sSelBoxMail

    ''' metodi per recuperare elementi delle mail '''

    def getMailList(self):
        return self.tIMAP_USER.getMailList(self.sSelBoxMail)

    def getMailFromId(self, sId):
        return self.tIMAP_USER.getMailFromId(sId)

    def getUrlFromEmail(self, sId):
        return self.tIMAP_USER.getUrlFromEmail(sId)
