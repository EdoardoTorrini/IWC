
from urllib.parse import urlencode

from mail.models import Users
from django.views import View
from django.shortcuts import render, redirect


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
