

from urllib.parse import urlencode

from django.shortcuts import render, redirect
from django.views import View

from django.conf import settings
from mail.models import Users


class HomeMailView(View):

    def get(self, request):

        sToken = str( request.GET.get("token") )

        USER = Users.objects.all().filter(token=sToken)[0]
        context = {
            "token": sToken,
            "mail": [],
            "boxes": [],
            "form": None,
            "mail_sent": False,
            "user": USER.email
        }

        objIMAP = settings.IMAP_MANAGER.get(sToken)
        for id, box in objIMAP.getMailBoxes().items():
            context["boxes"].append({id: box})

        for mail in objIMAP.getMailList():
            context["mail"].append(
                {
                    "messid": mail.mailId,
                    "date": mail.date.strftime("%d %b"),
                    "subject": mail.subject,
                    "from": str( mail.sender)[:mail.sender.find(" <") ],
                    "to": eval(mail.to)
                }
            )

        context["mail"].reverse()

        if objIMAP.sSelBoxMail == '"[Gmail]/Posta inviata"':
            context["mail_sent"] = True

        return render(request, "mail/index.html", context)

    def post(self, request):

        sToken = str( request.POST.get("token") )
        sIdBox = str( request.POST.get("box") )

        objIMAP = settings.IMAP_MANAGER.get(sToken)
        objIMAP.setBoxMail(sIdBox)

        context = {
            "token": sToken
        }

        sBaseUrl = "../home/"
        sEncodedUrl = "{}?{}".format(sBaseUrl, urlencode(context))
        return redirect(sEncodedUrl, method="GET")
