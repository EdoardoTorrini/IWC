
from mail.models import Users
from django.views import View
from urllib.parse import urlencode


from django.shortcuts import redirect


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
