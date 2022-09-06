from threading import Thread
import smtplib

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

    def run(self):

        try:
            self.oServer.login(self.sEmailFrom, self.sPwd)
            msgEmail = self.createEmail()
            self.oServer.sendmail(
                self.sEmailFrom,
                ", ".join(self.aEmailDest),
                msgEmail.as_string()
            )

        except NameError:
            # TODO: aggiungi gestione errore
            pass
        except Exception as sErr:
            # TODO: aggiungi gestione errore
            pass

    def createEmail(self):

        msgEmail = MIMEMultipart()

        try:
            if self.sEmailFrom is not None and self.sEmailFrom != "":
                msgEmail["From"] = self.sEmailFrom

            ''' attach the list of the recivers email address '''
            if len( self.aEmailDest ) > 0:
                msgEmail["To"] = ", ".join(self.aEmailDest)

            ''' attach the list of the recivers email address put in the CC '''
            if len( self.aEmailCC ) > 0:
                msgEmail["CC"] = ", ".join(self.aEmailCC)

            ''' attach the list of the recivers email address put in the CCn '''
            if len( self.aEmailCCn ) > 0:
                msgEmail["CCn"] = ", ".join(self.aEmailCCn)

            ''' attach the Object of the mail '''
            if self.sObj is not None and self.sObj != "":
                msgEmail["Subject"] = self.sObj

            ''' attach the Body of the mail '''
            if self.sBody is not None and self.sBody != "":
                msgEmail.attach(
                    MIMEText("<b>Vediamo se funziona con due mail</b>", "html")
                )

            if len( self.aFile ) > 0:
                for file in self.aFile:
                    est = file

                    if est in ["png", "jpg", "jpeg"]:
                        with open(file, "rb") as fImg:
                            img = MIMEImage(fImg.read())
                            img.add_header('Content-Disposition', 'attachment', filename=file)
                            msgEmail.attach(img)

                    if est == "pdf":
                        pdf = MIMEApplication(open(file, "rb").read())
                        pdf.add_header('Content-Disposition', 'attachment', filename=pdf)
                        msgEmail.attach(pdf)

        except NameError:
            # TODO: gestione errore
            pass

        return msgEmail
