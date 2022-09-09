from threading import Thread
import imaplib
import email
import os

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.core.files import File


class ImapDownloadAttachFile(Thread):

    def __init__(self, sToken, sIdMail, sBox):
        super(ImapDownloadAttachFile, self).__init__(daemon=True)

        self.sToken = sToken
        self.sIdMail = sIdMail
        self.sBox = sBox
        self.oImap = None

    def run(self):

        from mail.models import Document, Users

        USER = Users.objects.all().get(token=self.sToken)

        self.oImap = imaplib.IMAP4_SSL("imap.gmail.com")
        self.oImap.login(user=USER.email, password=USER.password)
        self.oImap.select(self.sBox)

        try:
            typ, data = self.oImap.search(None, '(HEADER Message-ID "%s")' % self.sIdMail)
            nMess = data[0].decode('utf-8')

            oFss = FileSystemStorage()

            res, msg = self.oImap.fetch(str(nMess), "(RFC822)")
            for response in msg:
                if isinstance(response, tuple):
                    msg = email.message_from_bytes(response[1])

                    for part in msg.walk():
                        if part.get_filename() is not None:

                            sPath = os.path.join(settings.TEMP_ROOT, part.get_filename())
                            with open(sPath, "wb") as fSave:
                                fSave.write(part.get_payload(decode=True))

                            fSave = File(open(sPath, "rb"))

                            fPc = oFss.save(
                                part.get_filename(), fSave
                            )
                            fUrl = oFss.url(fPc)

                            fSave.close()
                            os.remove(sPath)

                            print(self.sToken, fPc, fUrl, part.get_filename())

        except Exception as sErr:
            print(sErr)

