
from django.views import View
from django.conf import settings
from django.shortcuts import render

from IWC.my_lib import StringElaborator
from mail.models import Users


class MailInspector(View):

    def get(self, request):

        sToken = str( request.GET.get("token") )
        sMailId = str( request.GET.get("messid") )

        USER = Users.objects.all().filter(token=sToken)[0]

        objIMAP = settings.IMAP_MANAGER.get(sToken)
        oMail = objIMAP.getMailFromId(sMailId)

        dFile = {}
        if len(oMail.file) > 0:
            dFile = objIMAP.getUrlFromEmail(sMailId)

        context = {
            "token": sToken,
            "mail_id": sMailId,
            "body": StringElaborator(str( oMail.body )).getPlainText(),
            "date": oMail.date,
            "subject": oMail.subject,
            "from": oMail.sender,
            "to": oMail.to.strip('][').split(', '),
            "cc": oMail.cc.strip('][').split(', '),
            "boxes": [],
            "file": dFile,
            "user": USER.email
        }

        objIMAP = settings.IMAP_MANAGER.get(sToken)
        for id, box in objIMAP.getMailBoxes().items():
            context["boxes"].append({id: box})

        return render(request, "mail/mail.html", context)
