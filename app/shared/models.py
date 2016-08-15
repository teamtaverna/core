from __future__ import unicode_literals

from django.db import models


class TimestampMixin(models.Model):
    """Mixin for date and timestamp."""

    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
