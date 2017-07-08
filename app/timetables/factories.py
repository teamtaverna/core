import datetime

from django.contrib.auth import get_user_model
from django.utils import timezone

import factory
from factory.django import DjangoModelFactory

from . import models
from common.mixins import TimestampMixin


class TimestampFactory(DjangoModelFactory):
    """TimestampMixin model factory."""

    class Meta:
        model = TimestampMixin
        abstract = True

    date_created = timezone.make_aware(timezone.datetime(2008, 1, 1, 0, 0, 0))
    date_modified = timezone.make_aware(timezone.datetime(2009, 1, 1, 0, 0, 0))


class WeekdayFactory(DjangoModelFactory):
    """Weekday model factory."""

    class Meta:
        model = models.Weekday

    name = 'Monday'


class MealFactory(DjangoModelFactory):
    """Meal model factory."""

    class Meta:
        model = models.Meal

    name = 'Breakfast'
    start_time = datetime.time(9, 0, 0)
    end_time = datetime.time(10, 0, 0)


class CourseFactory(DjangoModelFactory):
    """Course model factory."""

    class Meta:
        model = models.Course

    name = 'Appetizer'
    sequence_order = 0


class UserFactory(DjangoModelFactory):
    """Django admin user model factory."""

    class Meta:
        model = get_user_model()

    username = 'admin'
    email = 'admin@admin.com'
    password = 'adminpassword'
    is_superuser = True
    is_active = True


class TimetableFactory(TimestampFactory):
    """Timetable model factory."""

    class Meta:
        model = models.Timetable

    name = 'Fellows Timetable'
    cycle_length = 14
    ref_cycle_day = 2
    ref_cycle_date = datetime.date(2016, 10, 1)
    description = 'Some random description'


class TimetableManagementFactory(DjangoModelFactory):
    """Timetablemanagement model factory."""

    class Meta:
        model = models.TimetableManagement

    user = factory.SubFactory(UserFactory)
    timetable = factory.SubFactory(TimetableFactory)
    is_super = True


class UserWithTimetableFactory(DjangoModelFactory):
    """
    Factory specifying many-to-many through relationship.

    The 'admin' field in Timetable model is a many-to-many relationship
    to User model through Admin model.
    """

    admins = factory.RelatedFactory(TimetableManagementFactory, 'user')


class DishFactory(TimestampFactory):
    """Dish model factory."""

    class Meta:
        model = models.Dish

    name = 'Coconut rice'
    description = 'Some random description'


class MenuItemFactory(TimestampFactory):
    """MenuItem model factory."""

    class Meta:
        model = models.MenuItem

    timetable = factory.SubFactory(TimetableFactory)
    cycle_day = 2
    meal = factory.SubFactory(MealFactory)
    course = factory.SubFactory(CourseFactory)
    dish = factory.SubFactory(DishFactory)


class EventFactory(TimestampFactory):
    """Event model factory."""

    class Meta:
        model = models.Event

    name = 'Christmas'
    timetable = factory.SubFactory(TimetableFactory)
    action = 'no-meal'
    start_date = timezone.make_aware(timezone.datetime(2008, 12, 23, 0, 0, 0))
    end_date = timezone.make_aware(timezone.datetime(2008, 12, 28, 0, 0, 0))


class VendorFactory(DjangoModelFactory):
    """Vendor model Factory."""

    class Meta:
        model = models.Vendor

    name = 'Mama Taverna'
    info = 'Some random info'


class ServingFactory(TimestampFactory):
    """Serving model factory."""

    class Meta:
        model = models.Serving

    menu_item = factory.SubFactory(MenuItemFactory)
    vendor = factory.SubFactory(VendorFactory)
    date_served = datetime.date(2016, 10, 1)


class VendorServiceFactory(DjangoModelFactory):
    """VendorService model factory."""

    class Meta:
        model = models.VendorService

    timetable = factory.SubFactory(TimetableFactory)
    vendor = factory.SubFactory(VendorFactory)
    start_date = datetime.date(2008, 1, 23)
    end_date = datetime.date(2008, 12, 28)
