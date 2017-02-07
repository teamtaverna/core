from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _

from hashid_field import HashidField

from common.mixins import TimestampMixin
from common.utils import timestamp_seconds


class ApiKey(TimestampMixin):
    """Model representing clients' api keys."""

    token = HashidField(
        min_length=32,
        alphabet='0123456789abcdef',
        default=timestamp_seconds,
        unique=True,
        editable=False
    )
    revoked = models.BooleanField(default=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def clean(self):
        if not self.owner.is_superuser:
            raise ValidationError(_('Ensure the owner is a superuser.'))

        super().clean()

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.token.hashid
