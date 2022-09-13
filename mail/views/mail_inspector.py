
from django.views import View
from django.conf import settings
from django.shortcuts import render

from IWC.my_lib import StringElaborator, ImapDownloadAttachFile


class MailInspector(View):

    def get(self, request):

        sToken = str( request.GET.get("token") )
        sMailId = str( request.GET.get("messid") )

        objIMAP = settings.IMAP_MANAGER.get(sToken)
        oMail = objIMAP.getMailFromId(sMailId)

        dFile = {}
        if len(oMail.file) > 0:
            dFile = objIMAP.getUrlFromEmail(sMailId)

        context = {
            "token": sToken,
            "body": StringElaborator(str( oMail.body )).getPlainText(),
            "date": oMail.date,
            "subject": oMail.subject,
            "from": oMail.sender,
            "to": oMail.to.strip('][').split(', '),
            "cc": oMail.cc.strip('][').split(', '),
            "boxes": [],
            "file": dFile,
            "mailTo": []
        }

        objIMAP = settings.IMAP_MANAGER.get(sToken)
        for id, box in objIMAP.getMailBoxes().items():
            context["boxes"].append({id: box})

        return render(request, "mail/mail.html", context)
