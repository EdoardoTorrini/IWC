from threading import Thread
import imaplib
import email


class ImapMail(Thread):

    def __init__(self, sUser, sPwd, sBox):
        super(ImapMail, self).__init__(daemon=True)

        self.sUser = sUser
        self.sPwd = sPwd
        self.sBox = sBox

        self.oImap = None

        self.aBoxMail = []

    def connect(self):

        try:
            self.oImap = imaplib.IMAP4_SSL("imap.gmail.com")
            self.oImap.login(user=self.sUser, password=self.sPwd)
            self.oImap.select(self.sBox)

        except Exception as sErr:
            print(sErr)

    def run(self):

        self.connect()

        status, messages = self.oImap.select(self.sBox)

        nMess = int(messages[0].decode("utf-8"))

        for i in range(1, nMess + 1):
            res, msg = self.oImap.fetch(str(i), "(RFC822)")

            for response in msg:
                if isinstance(response, tuple):
                    msg = email.message_from_bytes(response[1])
                    aFile = []

                    sIdMess = msg["Message-ID"]
                    if sIdMess not in self.aBoxMail:
                        for part in msg.walk():
                            if part.get_filename() is not None:
                                aFile.append(part.get_filename())
                        msg["File"] = aFile
                        self.aBoxMail.append(msg)

    def getMailBoxes(self):
        return self.aBoxMail



