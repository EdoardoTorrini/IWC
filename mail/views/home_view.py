

from urllib.parse import urlencode

from django.shortcuts import render, redirect
from django.views import View

from django.conf import settings
from IWC.my_lib import DateTimeConverter


class HomeMailView(View):

    def get(self, request):

        sToken = str( request.GET.get("token") )

        context = {
            "token": sToken,
            "mail": [],
            "boxes": [],
            "form": None,
            "mail_sent": False
        }

        objIMAP = settings.IMAP_MANAGER.get(sToken)
        for id, box in objIMAP.getMailBoxes().items():
            context["boxes"].append({id: box})

        for sMailId, oMail in objIMAP.getMailDict().items():
            context["mail"].append(
                {
                    "messid": sMailId,
                    "date": DateTimeConverter(oMail["Date"], bEmail=True).getDateFormatted("%d %b"),
                    "subject": oMail["Subject"],
                    "from": str( oMail["From"])[:oMail["From"].find(" <") ],
                    "to": oMail["To"] # str( oMail["To"])[:oMail["To"].find(" <") ]
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
