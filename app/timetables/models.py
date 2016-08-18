from __future__ import unicode_literals

from django.db import models

from common.mixins import ForceCapitalizeMixin


class Weekday(ForceCapitalizeMixin, models.Model):
    """Model representing the day of the week."""

    name = models.CharField(max_length=60, unique=True)

    capitalized_field_names = ('name',)

    def __str__(self):
        return self.name


class Meal(ForceCapitalizeMixin, models.Model):
    """
    Model representing food occasions.

    This represents an occasion during the day that food
    is scheduled to be served. E.g breakfast, lunch, etc.
    """

    name = models.CharField(max_length=60, unique=True)
    start_time = models.TimeField()
    end_time = models.TimeField()

    capitalized_field_names = ('name',)

    def __str__(self):
        return self.name
