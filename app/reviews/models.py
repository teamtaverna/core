from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

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
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    serving = models.ForeignKey(Serving, on_delete=models.CASCADE)
    value = models.PositiveSmallIntegerField(choices=RATINGS)
    comment = models.TextField(blank=True)

    def __str__(self):
        return '{}\'s review of {}'.format(self.user, self.serving)

    class Meta:
        unique_together = ('user', 'serving')
