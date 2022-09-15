from threading import Thread
import os

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.core.files import File


class ImapDownloadAttachFile(Thread):

    def __init__(self, MAIL, fNew):
        super(ImapDownloadAttachFile, self).__init__(daemon=True)

        self.MAIL = MAIL
        self.fNew = fNew

    def run(self):

        from mail.models import Document

        try:
            oFss = FileSystemStorage()
            sPath = os.path.join(settings.TEMP_ROOT, self.fNew.get_filename())
            with open(sPath, "wb") as fSave:
                fSave.write(self.fNew.get_payload(decode=True))

            fSave = File(open(sPath, "rb"))

            fPc = oFss.save(
                self.fNew.get_filename(), fSave
            )
            fUrl = oFss.url(fPc)

            fSave.close()
            os.remove(sPath)
            sPath = os.path.join(settings.MEDIA_ROOT, self.fNew.get_filename())

            oDoc = Document(
                email=self.MAIL,
                path=sPath,
                serverPath=fUrl[1:],
                filename=self.fNew.get_filename()
            )

            oDoc.save()
            print("save new file:", oDoc.id)

        except Exception as sErr:
            print("IMAP_FILE:", sErr)
