
from urllib.parse import urlencode

from django.views import View
from django.shortcuts import redirect
from django.core.files.storage import FileSystemStorage

from IWC.my_lib import MySMTP
from mail.models import Users


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

        aFileList = []

        for file in request.FILES.getlist("document"):
            fss = FileSystemStorage()
            fPc = fss.save(file.name, file)
            fUrl = fss.url(fPc)
            aFileList.append(file.name)

        if sEmailDest.find(",") > -1:
            aEmailDest = [ mail for mail in sEmailDest.split(",") ]
        else:
            aEmailDest.append(sEmailDest)

        if len(sEmailCC) > 0:
            if sEmailCC.find(",") > -1:
                aEmailCC = [ mail for mail in sEmailCC.split(",") ]
            else:
                aEmailCC.append(sEmailCC)

        if len(sEmailCCn) > 0:
            if sEmailCCn.find(",") > -1:
                aEmailCCn = [ mail for mail in sEmailCCn.split(",") ]
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
            "aFile": aFileList
        }

        context = {
            "token": sToken
        }

        oSendEmail = MySMTP(dDati)
        oSendEmail.start()

        sBaseUrl = "../home/"
        sEncodedUrl = "{}?{}".format(sBaseUrl, urlencode(context))
        return redirect(sEncodedUrl, method="GET")
