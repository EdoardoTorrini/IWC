import mimetypes

from django.shortcuts import HttpResponse
from django.views import View

from mail.models import Document, Users, Email


class DownloadFile(View):

    def get(self, request):

        sToken = str( request.GET.get("token") )
        sMailId = str( request.GET.get("mail_id") )
        sFileName = str( request.GET.get("file_name") )

        USER = Users.objects.all().filter(token=sToken)[0]
        MAIL = Email.objects.all().filter(mailId=sMailId, user=USER)[0]
        DOC = Document.objects.all().filter(email=MAIL, filename=sFileName)[0]

        try:
            with open(DOC.path, "rb") as fOut:
                mimetype = mimetypes.guess_type(DOC.filename)

                if len(mimetype) > 1:
                    mimetype = mimetype[0]

                response = HttpResponse(fOut, content_type=mimetype)
                response["Content-Disposition"] = "attachment; filename={}".format(DOC.filename)

        except Exception as sErr:
            print(sErr)

        return response



