
from django.db import models
from uuid import uuid4


class Users(models.Model):

    token = models.CharField(max_length=255, default=uuid4(), primary_key=True)
    csrfToken = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)

    def __str__(self):
        return "{}|{}|{}|{}".format(
            self.token,
            self.email,
            self.password,
            self.csrfToken
        )