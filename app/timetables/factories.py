import datetime

import factory
from django.contrib.auth import get_user_model
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


class UserFactory(DjangoModelFactory):
    """Django admin user model factory."""

    class Meta:
        model = get_user_model()
        django_get_or_create = ('username', 'email', 'password')

    username = 'admin'
    email = 'admin@admin.com'
    password = 'adminpassword'
    is_superuser = True
    is_active = True


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


class AdminFactory(DjangoModelFactory):
    """Admin model factory."""

    class Meta:
        model = models.Admin

    user = factory.SubFactory(UserFactory)
    timetable = factory.SubFactory(TimetableFactory)
    is_super = True


class UserWithTimetableFactory(DjangoModelFactory):
    """
    Factory specifying many-to-many through relationship.

    The 'admin' field in Timetable model is a many-to-many relationship
    to User model through Admin model.
    """

    admins = factory.RelatedFactory(AdminFactory, 'user')
