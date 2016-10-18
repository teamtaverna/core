from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

from common.mixins import TimestampMixin
from app.timetables.models import Serving


class Review(TimestampMixin):
    """
    Model representing ratings and comments
    submitted by users for menu item
    they had on a particular day of the cycle.
    """

    RATINGS = (
        (5, 'EXCELLENT'),
        (4, 'GOOD'),
        (3, 'FAIR'),
        (2, 'POOR'),
        (1, 'TERRIBLE')
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    serving = models.ForeignKey(Serving, on_delete=models.CASCADE)
    value = models.PositiveSmallIntegerField(choices=RATINGS)
    comment = models.TextField(blank=True)

    def __str__(self):
        return '{}\'s review of {}'.format(self.user, self.serving)

    class Meta:
        unique_together = ('user', 'serving')
