from urllib.parse import urlencode

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.conf import settings

# Create your views here.

from mail.models import *
from datetime import datetime
import hashlib
from IWC.my_lib import StringElaborator, DateTimeConverter


class LoginMailView(View):

    def get(self, request):

        context = {
            "token": "",
            "redirect": True
        }

        mUser = Users.objects.all().filter(csrfToken=request.COOKIES.get("csrftoken"))
        if mUser.count() > 0:
            context["token"] = mUser[0].token

            sBaseUrl = "../home/"
            sEncodedUrl = "{}?{}".format(sBaseUrl, urlencode(context))
            return redirect(sEncodedUrl, method="GET")
        else:
            return render(request, "mail/login.html", { "error": request.GET.get("error") is not None })


class CheckLogin(View):

    def post(self, request):

        context = {
            "user": None,
            "error": False,
            "token": None
        }

        sUser = str( request.POST.get("email") )
        sPwd = str( request.POST.get("password") )
        sCrsfToken = str( request.COOKIES.get("csrftoken") )
        sToken = str( request.COOKIES.get("token") )

        if Users.objects.all().filter(email=sUser):
            if Users.objects.all().filter(email=sUser, password=sPwd):

                USER = Users.objects.all().filter(
                    email=sUser,
                    password=sPwd
                    # hashlib.sha256(sPwd.encode()) --> per averla criptata
                )[0]

                USER.csrftoken = sCrsfToken
                context["token"] = USER.token

                USER.save()

            else:
                context["error"] = True
                sBaseUrl = "../login/"
                sEncodedUrl = "{}?{}".format(sBaseUrl, urlencode(context))
                return redirect(sEncodedUrl, method="GET")

        else:
            USER = Users(
                csrfToken=sCrsfToken,
                email=sUser,
                password=sPwd
            )
            USER.save()
            context["token"] = USER.token
            context["user"] = sUser

            # creare nello stack il nuovo utente e avviare il thread 

        sBaseUrl = "../home/"
        sEncodedUrl = "{}?{}".format(sBaseUrl, urlencode(context))
        return redirect(sEncodedUrl, method="GET")


class HomeMailView(View):

    def get(self, request):

        sToken = str( request.GET.get("token") )

        context = {
            "token": sToken,
            "mail": [],
            "boxes": []
        }

        objIMAP = settings.IMAP_MANAGER.get(sToken)
        for box in objIMAP.getMailBoxes():
            for elem in box.split(" "):
                if elem.find("INBOX") > -1 or elem.find("[") > -1:
                    context["boxes"].append(elem)

        for sMailId, oMail in objIMAP.getMailDict().items():
            context["mail"].append(
                {
                    "messid": sMailId,
                    "date": DateTimeConverter(oMail["Date"], bEmail=True).getDateFormatted("%m/%d/%Y, %H:%M:%S"),
                    "subject": oMail["Subject"],
                    "from": str( oMail["From"])[:oMail["From"].find(" <") ]
                }
            )

        return render(request, "mail/index.html", context)


class MailInspector(View):

    def get(self, request, ):

        sToken = str( request.GET.get("token") )
        sMailId = str( request.GET.get("messid") )

        objIMAP = settings.IMAP_MANAGER.get(sToken)
        oMail = objIMAP.getMailDict().get(sMailId)

        context = {
            "token": sToken,
            "body": StringElaborator(str( objIMAP.readMessageFromId(sMailId) )).getPlainText(),
            "date": oMail["Date"],
            "subject": oMail["Subject"],
            "from": oMail["From"]
        }

        return HttpResponse(context["body"])


class MailSender(View):

    def post(self, request):

        sToken = str( request.POST.get("token") )
