from django.db.models.query import QuerySet


class APIMail:

    def __init__(self, sToken):
        self.sToken = sToken

    def getMailList(self, sBox):

        from mail.models import Users, Email

        USER = Users.objects.all().filter(token=self.sToken)[0]
        EMAILS = Email.objects.all().filter(user=USER, box=sBox)
        aRet = []

        if isinstance(EMAILS, QuerySet):
            for email in EMAILS:
                aRet.append(email)

        return aRet

    def getMailFromId(self, sId):

        from mail.models import Users, Email

        USER = Users.objects.all().filter(token=self.sToken)[0]
        EMAIL = Email.objects.all().filter(mailId=sId, user=USER)[0]
        return EMAIL

    def getUrlFromEmail(self, sId):

        from mail.models import Users, Email, Document

        USER = Users.objects.all().filter(token=self.sToken)[0]
        EMAIL = Email.objects.all().filter(mailId=sId, user=USER)[0]
        DOC = Document.objects.all().filter(email=EMAIL)
        aRet = []

        if isinstance(DOC, QuerySet):
            for file in DOC:
                aRet.append({"name": file.filename, "url": file.serverPath})

        return aRet

