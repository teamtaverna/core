from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from common.mixins import TimestampMixin
from app.timetables.models import Serving


class Review(TimestampMixin):
    """Model representing ratings and comments on served menu items."""

    EXCELLENT = 5
    GOOD = 4
    FAIR = 3
    POOR = 2
    TERRIBLE = 1

    RATINGS = (
        (EXCELLENT, 'EXCELLENT'),
        (GOOD, 'GOOD'),
        (FAIR, 'FAIR'),
        (POOR, 'POOR'),
        (TERRIBLE, 'TERRIBLE')
    )

    # Make nullable for anonymity of reviewers.
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, blank=True, null=True
    )
    # anonymity_id is just a hashed unique identifier for the reviewer used
    # as a check prevent multiple reviews from one person
    anonymity_id = models.CharField(blank=True, null=True, max_length=250)
    serving = models.ForeignKey(Serving, on_delete=models.CASCADE)
    value = models.PositiveSmallIntegerField(choices=RATINGS)
    comment = models.TextField(blank=True)

    def __str__(self):
        return '{}\'s review of {}'.format(
            self.user or self.anonymity_id, self.serving
        )

    def clean(self):
        if self.user:
            if self.__class__.objects.filter(
                user=self.user, serving=self.serving
            ).exists():
                raise ValidationError(_('user and serving must be unique'))
        if self.anonymity_id:
            if self.__class__.objects.filter(
                anonymity_id=self.anonymity_id, serving=self.serving
            ).exists():
                raise ValidationError(
                    _('anonymity_id and serving must be unique')
                )
        super().clean()

    def save(self, *args, **kwargs):
        self.clean()
        return super().save(*args, **kwargs)
