
from django.db import models
from IWC.my_lib import SeparateValueField
from . import Users


class Email(models.Model):

    mailId = models.CharField(max_length=255, primary_key=True)
    user = models.ForeignKey(
        Users,
        on_delete=models.CASCADE,
        related_name="%(class)s_Users"
    )
    box = models.CharField(max_length=255)

    sender = models.CharField(max_length=255, null=False)
    to = SeparateValueField()
    cc = SeparateValueField()
    ccn = models.CharField(max_length=255, null=False)
    subject = models.CharField(max_length=255, null=False)
    date = models.DateField()
    contentType = models.CharField(max_length=255, null=False)
    body = models.CharField(max_length=255, null=False)
    file = SeparateValueField()

    def __str__(self):
        return "{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}".format(
            self.mailId,
            self.user.token,
            self.sender,
            self.to,
            self.cc,
            self.ccn,
            self.subject,
            self.date,
            self.contentType,
            self.body,
            self.file
        )
