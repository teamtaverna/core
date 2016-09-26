from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _

from common.mixins import SlugifyMixin, TimestampMixin


class Weekday(SlugifyMixin, models.Model):
    """Model representing the day of the week."""

    name = models.CharField(max_length=60)
    slug = models.SlugField(max_length=60, unique=True, null=True, editable=False)

    slugify_field = 'name'

    def __str__(self):
        return self.name


class Meal(SlugifyMixin, models.Model):
    """
    Model representing food occasions.

    This represents an occasion during the day that food
    is scheduled to be served. E.g breakfast, lunch, etc.
    """

    name = models.CharField(max_length=60)
    slug = models.SlugField(max_length=60, unique=True, null=True, editable=False)
    start_time = models.TimeField()
    end_time = models.TimeField()

    slugify_field = 'name'

    def clean(self):
        if self.start_time >= self.end_time:
            raise ValidationError(_('start_time must be less than end_time.'))

        super().clean()

    def __str__(self):
        return self.name


class MealOption(SlugifyMixin, models.Model):
    """Model representing course/dish combinations to be served during a given meal."""

    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=120, unique=True, null=True, editable=False)

    slugify_field = 'name'

    def __str__(self):
        return self.name


class Course(SlugifyMixin, models.Model):
    """Model representing the particular dish served as one of the parts of a meal option."""

    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=150, unique=True, null=True, editable=False)

    slugify_field = 'name'

    def __str__(self):
        return self.name


class Timetable(SlugifyMixin, TimestampMixin):
    """
    Central model of the platform.

    It represents/encapsulates the entire structure and
    scheduling of meals, menu-items, dishes, courses, options etc,
    served at a location, to a team or the entire organisation.
    """

    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, null=True, editable=False)
    code = models.CharField(max_length=60, unique=True)
    api_key = models.CharField(max_length=255, unique=True)
    cycle_length = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)]
    )
    current_cycle_day = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)]
    )
    description = models.TextField(blank=True)
    admins = models.ManyToManyField(User, through='Admin')

    slugify_field = 'name'

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


class Dish(SlugifyMixin, TimestampMixin):
    """
    Model representing the actual food served.

    A dish represents the actual food served as a given
    course under an option of a meal on a cycle day in a timetable.
    E.g, Coconut rice garnished with fish stew and chicken or just
    Ice-cream.
    """

    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, null=True, editable=False)
    description = models.TextField(blank=True)

    slugify_field = 'name'

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Dishes'


class Admin(models.Model):
    """Model representing timetables' administratorship"""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timetable = models.ForeignKey(Timetable, on_delete=models.CASCADE)
    is_super = models.BooleanField()

    def __str__(self):
        return self.user.username

    class Meta:
        unique_together = ('user', 'timetable')


class MenuItem(TimestampMixin):
    """
    Model representing a Menu Item.

    A MenuItem represents the particular meal combination option that is to be
    served on a given cycle-day of a particular timetable.
    """

    timetable = models.ForeignKey(Timetable, on_delete=models.CASCADE)
    cycle_day = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)]
    )
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    meal_option = models.ForeignKey(MealOption, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        # Calling full_clean instead of clean to ensure validators are called
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return '{0} {1}'.format(self.cycle_day, self.meal)

    class Meta:
        unique_together = ('timetable', 'cycle_day', 'meal', 'meal_option')
