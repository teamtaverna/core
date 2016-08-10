from __future__ import unicode_literals

from django.db import models

class CommonInfo(models.Model):
    date_created = models.DateTimeField(auto_now=False, auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True, auto_now_add=False)

    class Meta:
        abstract = True
        