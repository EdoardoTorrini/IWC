from django.apps import AppConfig
from django.conf import settings

import sys
# if you need manage.py shell you have to comment the line below
from IWC.my_lib import ImapStack


class MailConfig(AppConfig):

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mail'

    def ready(self):

        if settings.IMAP_MANAGER is None:
            if 'runserver' not in sys.argv:
                return True

            settings.IMAP_MANAGER = ImapStack()
            from .models import Users

            for user in Users.objects.all():
                if user.email is not None and user.password is not None:
                    settings.IMAP_MANAGER.push(user.token, user.email, user.password)
                else:
                    # TODO: implementare gestione dell'errore
                    pass
