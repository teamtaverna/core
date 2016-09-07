from __future__ import unicode_literals

from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MinValueValidator

from common.mixins import ForceCapitalizeMixin, TimestampMixin


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

    def clean(self):
        if self.start_time >= self.end_time:
            raise ValidationError(_('start_time must be less than end_time.'))
        super().clean()

    def __str__(self):
        return self.name


class MealOption(ForceCapitalizeMixin, models.Model):
    name = models.CharField(max_length=120, unique=True)

    capitalized_field_names = ('name',)

    def __str__(self):
        return self.name


class Course(ForceCapitalizeMixin, models.Model):
    name = models.CharField(max_length=150, unique=True)

    capitalized_field_names = ('name',)

    def __str__(self):
        return self.name


class Timetable(TimestampMixin):
    """
    A timetable is the central entity or model of the platform.

    It represents/encapsulates the entire structure and
    scheduling of meals, menu-items, dishes, courses, options etc,
    served at a location, to a team or the entire organisation.
    """

    name = models.CharField(max_length=255, unique=True)
    code = models.CharField(max_length=60, unique=True)
    api_key = models.CharField(max_length=255, unique=True)
    cycle_length = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)]
    )
    current_cycle_day = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)]
    )

    def clean(self):
        # Ensure current_cycle_day and cycle_length are not None before compare
        if self.current_cycle_day and self.cycle_length:
            if self.current_cycle_day > self.cycle_length:
                raise ValidationError(_(
                    'Ensure Current cycle day is not greater than Cycle length.')
                )

        super().clean()

    def save(self, *args, **kwargs):
        # Calling full_clean instead of clean to ensure validators are called
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name
