from urllib.parse import urlencode

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.conf import settings

# Create your views here.
from django.views.generic import TemplateView

from mail.models import *
from IWC.my_lib import StringElaborator, DateTimeConverter

# Needs for the save of the file to send
from django.core.files.storage import FileSystemStorage


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

                USER.csrfToken = sCrsfToken
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
            "boxes": [],
            "form": None
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
                    "from": str( oMail["From"])[:oMail["From"].find(" <") ]
                }
            )

        return render(request, "mail/index.html", context)

    def post(self, request):

        sToken = str( request.POST.get("token") )
        sIdBox = str( request.POST.get("box") )

        objIMAP = settings.IMAP_MANAGER.get(sToken)
        objIMAP.setReadBox(sIdBox)

        context = {
            "token": sToken
        }

        sBaseUrl = "../home/"
        sEncodedUrl = "{}?{}".format(sBaseUrl, urlencode(context))
        return redirect(sEncodedUrl, method="GET")


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
            "from": oMail["From"],
            "boxes": []
        }

        objIMAP = settings.IMAP_MANAGER.get(sToken)
        for id, box in objIMAP.getMailBoxes().items():
            context["boxes"].append({id: box})

        return render(request, "mail/mail.html", context)
        # return HttpResponse(context["body"])


class MailSender(View):

    def post(self, request):

        sToken = str( request.POST.get("token") )

        sEmailDest, aEmailDest = str( request.POST.get("emailListDest") ), []
        sEmailCC, aEmailCC = str( request.POST.get("emailListCc") ), []
        sEmailCCn, aEmailCCn = str( request.POST.get("emailListCcn") ), []

        sObj = str( request.POST.get("emailObj") )
        sBody = str( request.POST.get("body") )

        mUser = Users.objects.all().filter(token=sToken)
        sEmailFrom = mUser[0].email
        sPwd = mUser[0].password

        for file in request.FILES.getlist("document"):
            fss = FileSystemStorage()
            fPc = fss.save(file.name, file)
            fUrl = fss.url(fPc)

        if sEmailDest.find(";") > -1:
            aEmailDest = [ mail for mail in sEmailDest.split(";") ]
        else:
            aEmailDest.append(sEmailDest)

        if len(sEmailCC) > 0:
            if sEmailCC.find(";") > -1:
                aEmailCC = [ mail for mail in sEmailCC.split(";") ]
            else:
                aEmailCC.append(sEmailCC)

        if len(sEmailCCn) > 0:
            if sEmailCCn.find(";") > -1:
                aEmailCCn = [ mail for mail in sEmailCCn.split(";") ]
            else:
                aEmailCCn.append(sEmailCCn)

        dDati = {
            "aEmailDest": aEmailDest,
            "aEmailCC": aEmailCC,
            "aEmailCCn": aEmailCCn,
            "sEmailFrom": sEmailFrom,
            "sPwd": sPwd,
            "sObj": sObj,
            "sBody": sBody,
            "aFile": []
        }

        context = {
            "token": sToken
        }

        sBaseUrl = "../home/"
        sEncodedUrl = "{}?{}".format(sBaseUrl, urlencode(context))
        return redirect(sEncodedUrl, method="GET")
