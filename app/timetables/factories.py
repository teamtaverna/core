import datetime

import factory
from django.contrib.auth.models import User
from django.utils.text import slugify
from factory.django import DjangoModelFactory

from . import models


class WeekdayFactory(DjangoModelFactory):
    """Weekday model factory."""

    class Meta:
        model = models.Weekday

    name = 'Monday'
    slug = factory.LazyAttribute(lambda obj: '%s' % slugify(obj.name))


class MealFactory(DjangoModelFactory):
    """Meal model factory."""

    class Meta:
        model = models.Meal

    name = 'Breakfast'
    slug = factory.LazyAttribute(lambda obj: '%s' % slugify(obj.name))
    start_time = datetime.time(5, 7, 9)
    end_time = datetime.time(6, 7, 9)


class MealOptionFactory(DjangoModelFactory):
    """MealOption model factory."""

    class Meta:
        model = models.MealOption

    name = 'Option A'
    slug = factory.LazyAttribute(lambda obj: '%s' % slugify(obj.name))


class CourseFactory(DjangoModelFactory):
    """Course model factory."""

    class Meta:
        model = models.Course

    name = 'Appetizer'
    slug = factory.LazyAttribute(lambda obj: '%s' % slugify(obj.name))


# Continue from here
class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    name = "John Doe"


class AdminFactory(DjangoModelFactory):
    class Meta:
        model = models.Admin

    user = ''
    timetable = ''
    is_super = True


class TimetableFactory(DjangoModelFactory):
    """Timetable model factory."""

    class Meta:
        model = models.Timetable

    name = 'Fellows Timetable'
    slug = factory.LazyAttribute(lambda obj: '%s' % slugify(obj.name))
    code = 'FT7876'
    api_key = 'TF78993jTY'
    cycle_length = 14
    current_cycle_day = 2
    description = 'Some random description'
    admins = ''


#     admins = models.ManyToManyField(User, through='Admin')


# class Admin(models.Model):
#     """Model representing timetables' administratorship"""

#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     timetable = models.ForeignKey(Timetable, on_delete=models.CASCADE)
#     is_super = models.BooleanField()
