import datetime

from django.contrib.auth import get_user_model
from django.utils.text import slugify
import factory
from factory.django import DjangoModelFactory

from . import models
from common.mixins import TimestampMixin


class TimestampFactory(DjangoModelFactory):
    """TimestampMixin model factory."""

    class Meta:
        model = TimestampMixin
        abstract = True

    date_created = datetime.datetime(2008, 1, 1, 0, 0, 0, tzinfo=datetime.timezone.utc)
    date_modified = datetime.datetime(2009, 1, 1, 0, 0, 0, tzinfo=datetime.timezone.utc)


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


class TimetableFactory(TimestampFactory):
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

    admins = factory.RelatedFactory(AdminFactory, 'user')


class DishFactory(TimestampFactory):
    """Dish model factory."""

    class Meta:
        model = models.Dish

    name = 'Coconut rice'
    slug = factory.LazyAttribute(lambda obj: '%s' % slugify(obj.name))
    description = 'Some random description'


class MenuItem(TimestampFactory):
    """MenuItem model factory."""

    class Meta:
        model = models.MenuItem

    timetable = factory.SubFactory(TimetableFactory)
    cycle_day = 2
    meal = factory.SubFactory(MealFactory)
    meal_option = factory.SubFactory(MealOptionFactory)


class EventFactory(TimestampFactory):
    """Event model factory."""

    class Meta:
        model = models.Event

    name = 'Christmas'
    timetable = factory.SubFactory(TimetableFactory)
    start_date = datetime.datetime(2008, 12, 23, 0, 0, 0, tzinfo=datetime.timezone.utc)
    end_date = datetime.datetime(2008, 12, 28, 0, 0, 0, tzinfo=datetime.timezone.utc)


class VendorFactory(DjangoModelFactory):
    """Vendor model Factory."""

    class Meta:
        model = models.Vendor

    name = 'Mama Taverna'
    slug = factory.LazyAttribute(lambda obj: '%s' % slugify(obj.name))
    info = 'Some random info'
    start_date = datetime.datetime(2008, 1, 23, 0, 0, 0, tzinfo=datetime.timezone.utc)
    end_date = datetime.datetime(2008, 12, 28, 0, 0, 0, tzinfo=datetime.timezone.utc)
