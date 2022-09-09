
from django.views import View
from django.conf import settings
from django.shortcuts import render

from IWC.my_lib import StringElaborator, ImapDownloadAttachFile


class MailInspector(View):

    def get(self, request):

        sToken = str( request.GET.get("token") )
        sMailId = str( request.GET.get("messid") )

        objIMAP = settings.IMAP_MANAGER.get(sToken)
        oMail = objIMAP.getMailDict().get(sMailId)

        context = {
            "token": sToken,
            "body": StringElaborator(str( objIMAP.readMessageFromId(sMailId) )).getPlainText(),
            "date": oMail["Date"],
            "subject": oMail["Subject"],
            "from": oMail["From"],
            "cc": oMail["CC"],
            "boxes": [],
            "file": oMail["File"],
            "mailTo": []
        }

        if len(oMail["File"]) > 0:
            ImapDownloadAttachFile(sToken, sMailId, objIMAP.getCurrentBoxMail()).start()

        if oMail["To"] is not None:
            context["mailTo"] += oMail["To"].split(",")

        if oMail["CC"] is not None:
            context["mailTo"] += oMail["CC"].split(",")

        objIMAP = settings.IMAP_MANAGER.get(sToken)
        for id, box in objIMAP.getMailBoxes().items():
            context["boxes"].append({id: box})

        return render(request, "mail/mail.html", context)
