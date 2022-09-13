
from django.db import models
from . import Email


class Document(models.Model):

    email = models.ForeignKey(Email, on_delete=models.CASCADE)

    path = models.CharField(max_length=255)
    serverPath = models.CharField(max_length=255)
    filename = models.CharField(max_length=255)

    def __str__(self):
        return "{}|{}|{}|{}".format(
            self.email.mailId,
            self.path,
            self.serverPath,
            self.filename
        )