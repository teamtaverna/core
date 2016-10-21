from __future__ import unicode_literals

from django.apps import AppConfig
from django.db.models.signals import post_save


class AccountsConfig(AppConfig):
    name = 'app.accounts'

    def ready(self):
        from django.contrib.auth.models import User
        from .signals import create_user_profile
        post_save.connect(create_user_profile, sender=User)
