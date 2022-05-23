from django.db import models
from uuid import uuid4

# Create your models here.


class Users(models.Model):

    token = models.CharField(max_length=255, default=uuid4())
    csrfToken = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)

    def __str__(self):
        return "{}|{}|{}|{}|".format(
            self.id,
            self.token,
            self.email,
            self.password
        )