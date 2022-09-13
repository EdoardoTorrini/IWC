from threading import Thread
import email
from email import utils
import time
from datetime import datetime as dt

from . import StringElaborator, ImapDownloadAttachFile


class ImapMail(Thread):

    def __init__(self, aMsg, sToken, sBox):
        super(ImapMail, self).__init__(daemon=True)

        self.aMsg = aMsg
        self.sToken = sToken
        self.sBox = sBox

    def run(self):

        from mail.models import Email, Users

        try:
            if isinstance(self.aMsg, list):
                for response in self.aMsg:
                    if isinstance(response, tuple):
                        msg = email.message_from_bytes(response[1])

                        EMAIL = Email.objects.all().filter(mailId=msg["Message-ID"])
                        if len(EMAIL) > 0:
                            break

                        ''' gestione del body '''
                        sTmp = ""
                        if msg.is_multipart():
                            sTmp = msg.get_payload(0)
                        else:
                            sTmp = msg.get_payload(None, True)

                        ''' gestione dei vuoti '''
                        aTo, aCC, aCCn = [], [], []
                        if msg["To"] is not None:
                            aTo = msg["To"].split(",")

                        if msg["CC"] is not None:
                            aCC = msg["CC"].split(",")

                        if msg["CCn"] is not None:
                            aCCn = msg["CCn"].split(",")

                        ''' gestione dei file collegati '''
                        aTmp = []
                        for part in msg.walk():
                            if part.get_filename() is not None:
                                aTmp.append(part.get_filename())

                        ''' gestione della data '''
                        dData = dt.fromtimestamp(
                            time.mktime(utils.parsedate(msg["Date"]))
                        )

                        USER = Users.objects.all().filter(token=self.sToken)[0]
                        oMail = Email(
                            mailId=msg["Message-ID"],
                            user=USER,
                            box=self.sBox,
                            sender=msg["From"],
                            to=aTo,
                            cc=aCC,
                            ccn=aCCn,
                            subject=msg["Subject"],
                            date=dData,
                            contentType=msg["Content-Type"],
                            body=str(sTmp),
                            file=aTmp
                        )

                        oMail.save()
                        print("Save new mail:", oMail.mailId)

                        for part in msg.walk():
                            if part.get_filename() is not None:
                                ImapDownloadAttachFile(oMail, part).start()

        except Exception as sErr:
            print("IMAP_MAIL:", sErr)
