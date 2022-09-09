from threading import Thread
import smtplib
import os
from django.conf import settings

from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart

from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.image import MIMEImage
'''
aEmailDest, aEmailCC, aEmailCCn, sEmailFrom, sPwd, sObj, sBody, aFile
'''


class MySMTP(Thread):

    def __init__(self, dParams):
        super().__init__(daemon=True)

        if isinstance(dParams, dict):
            for key, values in dParams.items():
                setattr(self, key, values)
        else:
            # TODO: inserisci errore
            pass

        self.oServer = smtplib.SMTP('smtp.gmail.com', 587)
        self.oServer.ehlo()
        self.oServer.starttls()

        self.mToSend = []

    def run(self):

        try:
            self.oServer.login(self.sEmailFrom, self.sPwd)
            msgEmail = self.createEmail()
            self.oServer.sendmail(
                self.sEmailFrom,
                self.mToSend,
                msgEmail.as_string()
            )

            print("invio mail effettuato")

        except NameError:
            # TODO: aggiungi gestione errore
            pass
        except Exception as sErr:
            # TODO: aggiungi gestione errore
            print(sErr)

    def createEmail(self):

        msgEmail = MIMEMultipart()
        try:
            if self.sEmailFrom is not None and self.sEmailFrom != "":
                msgEmail["From"] = self.sEmailFrom

            ''' attach the list of the recivers email address '''
            if len( self.aEmailDest ) > 0:
                msgEmail["To"] = ", ".join(self.aEmailDest)
                self.mToSend += self.aEmailDest

            ''' attach the list of the recivers email address put in the CC '''
            if len( self.aEmailCC ) > 0:
                msgEmail["CC"] = ", ".join(self.aEmailCC)
                self.mToSend += self.aEmailCC

            ''' attach the list of the recivers email address put in the CCn '''
            if len( self.aEmailCCn ) > 0:
                msgEmail["CCn"] = ", ".join(self.aEmailCCn)
                self.mToSend += self.aEmailCCn

            ''' attach the Object of the mail '''
            if self.sObj is not None and self.sObj != "":
                msgEmail["Subject"] = self.sObj

            ''' attach the Body of the mail '''
            if self.sBody is not None and self.sBody != "":
                msgEmail.attach(
                    MIMEText(self.sBody, "html")
                )

            if len( self.aFile ) > 0:
                for file in self.aFile:
                    est = file.split(".")[1]
                    path = settings.MEDIA_ROOT + "\\" + file

                    if est in ["png", "jpg", "jpeg"]:
                        if os.path.exists(path):
                            with open(path, "rb") as fImg:
                                img = MIMEImage(fImg.read())
                                img.add_header('Content-Disposition', 'attachment', filename=file)
                                msgEmail.attach(img)

                    else:
                        if os.path.exists(path):
                            fSend = MIMEApplication(open(path, "rb").read())
                            fSend.add_header('Content-Disposition', 'attachment', filename=file)
                            msgEmail.attach(fSend)

        except NameError:
            # TODO: gestione errore
            pass
        except Exception as sErr:
            print(sErr)

        return msgEmail
