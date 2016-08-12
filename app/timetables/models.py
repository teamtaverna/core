from __future__ import unicode_literals

from django.db import models


class Weekday(models.Model):
    """Model representing the day of the week."""

    name = models.CharField(max_length=60, unique=True)

    def clean(self):
        """
        Capitalize the first letter of the first word to avoid case
        insensitive duplicates for name field.
        """
        self.name = self.name.capitalize()

    def save(self, *args, **kwargs):
        self.clean()
        return super(Weekday, self).save(*args, **kwargs)


class Meal(models.Model):
    name = models.CharField(max_length=60, unique=True)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return self.name
