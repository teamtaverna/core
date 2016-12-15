from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.db.utils import IntegrityError
from django.utils.translation import ugettext_lazy as _

from hashid_field import HashidField

from common.mixins import SlugifyMixin, TimestampMixin
from common.utils import timestamp_seconds


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
        # Ensure start time and end time are not None before compare
        if self.start_time and self.end_time:
            if self.start_time >= self.end_time:
                raise ValidationError(_('start_time must be less than end_time.'))

        super().clean()

    def __str__(self):
        return self.name


class Course(SlugifyMixin, models.Model):
    """Model representing the sequence/order of different kind of dishes for a meal."""

    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=150, unique=True, null=True, editable=False)
    sequence_order = models.PositiveSmallIntegerField(unique=True)

    slugify_field = 'name'

    def __str__(self):
        return self.name


class Vendor(SlugifyMixin, models.Model):
    """Model representing food service-provider."""

    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, editable=False)
    info = models.TextField(blank=True)

    slugify_field = 'name'

    def __str__(self):
        return self.name


class Timetable(SlugifyMixin, TimestampMixin):
    """
    Central model of the platform.

    It represents/encapsulates the entire structure and
    scheduling of meals, menu-items, dishes, courses etc,
    served at a location, to a team or the entire organisation.
    """

    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, null=True, editable=False)
    code = models.CharField(max_length=60, unique=True)
    api_key = models.CharField(max_length=255, unique=True)
    cycle_length = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)]
    )
    ref_cycle_day = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)]
    )
    ref_cycle_date = models.DateTimeField()
    inactive_weekdays = models.ManyToManyField(Weekday)
    vendors = models.ManyToManyField(Vendor, through='VendorService')
    is_active = models.BooleanField(default=True)
    description = models.TextField(blank=True)
    admins = models.ManyToManyField(User, through='TimetableManagement')

    slugify_field = 'name'

    def clean(self):
        # Ensure ref_cycle_day and cycle_length are not None before compare
        if self.ref_cycle_day and self.cycle_length:
            if self.ref_cycle_day > self.cycle_length:
                raise ValidationError(_(
                    'Ensure Ref cycle day is not greater than Cycle length.')
                )

        super().clean()

    def save(self, *args, **kwargs):
        # Calling full_clean instead of clean to ensure validators are called
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def calculate_cycle_day(self, date_datetime):
        days_interval = (date_datetime - self.ref_cycle_date).days

        if days_interval < 0:
            raise ValidationError(
                _('Supply a date later than %s' % (self.ref_cycle_date))
            )

        cycle_day = (((days_interval % self.cycle_length) + self.ref_cycle_day)
                     % self.cycle_length)

        if cycle_day == 0:
            cycle_day = self.cycle_length

        return cycle_day

    def get_vendors(self, date_datetime):
        return [vendor for vendor in Vendor.objects.filter(
            timetable__slug=self.slug,
            vendorservice__start_date__lte=date_datetime,
            vendorservice__end_date__gte=date_datetime
        )]


class Dish(SlugifyMixin, TimestampMixin):
    """
    Model representing the actual food served.

    A dish represents the actual food served as a given
    course of a meal on a cycle day in a timetable.
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


class TimetableManagement(models.Model):
    """Model representing timetables' administratorship"""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timetable = models.ForeignKey(Timetable, on_delete=models.CASCADE)
    is_super = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    class Meta:
        unique_together = ('user', 'timetable')


class MenuItem(TimestampMixin):
    """
    Model representing a Menu Item.

    A MenuItem represents the particular meal combination that is to be
    served on a given cycle-day of a particular timetable.
    """

    timetable = models.ForeignKey(Timetable, on_delete=models.CASCADE)
    cycle_day = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)]
    )
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        # Calling full_clean instead of clean to ensure validators are called
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return 'Cycle {} {} for timetable {}'.format(
            self.cycle_day, self.meal, self.timetable
        )

    class Meta:
        unique_together = ('timetable', 'cycle_day', 'meal', 'course', 'dish')


class Event(TimestampMixin):
    """
    Model representing event.

    Event represent a date or range of dates to which a
    specific timetable will be active or functional.
    """

    NO_MEAL = 'no-meal'

    ACTION_CHOICES = (
        (NO_MEAL, 'no meal will be served'),
    )

    name = models.CharField(max_length=150)
    timetable = models.ForeignKey(Timetable, on_delete=models.CASCADE)
    action = models.CharField(max_length=255, choices=ACTION_CHOICES)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def clean(self):
        if self.start_date and self.end_date:
            if self.start_date >= self.end_date:
                raise ValidationError(_('Start date must be less than end date.'))
        super().clean()

    def save(self, *args, **kwargs):
        self.clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('name', 'start_date', 'end_date')


class Serving(TimestampMixin):
    """Model representing already served menu."""

    public_id = HashidField(
        alphabet='0123456789abcdefghijklmnopqrstuvwxyz',
        default=timestamp_seconds,
        unique=True
    )
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date_served = models.DateTimeField()

    def __str__(self):
        return '{} served on {}'.format(self.menu_item, self.date_served)

    class Meta:
        unique_together = ('menu_item', 'vendor', 'date_served')


class VendorService(models.Model):
    """Model representing tenure a vendor serves a specific timetable."""

    timetable = models.ForeignKey(Timetable, on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    start_date = models.DateTimeField(default=None, null=True, blank=True)
    end_date = models.DateTimeField(default=None, null=True, blank=True)

    def clean(self):
        if self.start_date and self.end_date:
            if self.end_date <= self.start_date:
                raise ValidationError(
                    _('Ensure end date is not less than or equal to start date.')
                )

        super().clean()

    def save(self, *args, **kwargs):
        # Calling full_clean instead of clean to ensure validators are called
        self.full_clean()

        return super().save(*args, **kwargs)

    def __str__(self):
        return '{} - {}'.format(self.timetable, self.vendor)

    class Meta:
        unique_together = ('timetable', 'vendor')


class ServingAutoUpdate(models.Model):
    """Model representing Automatic Update of Servings."""

    timetable = models.ForeignKey(Timetable, on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date = models.DateTimeField()

    @classmethod
    def get_servings(cls, timetable, vendor, date):
        try:
            cycle_day = timetable.calculate_cycle_day(date)
        except ValidationError:
            raise

        menu_items = MenuItem.objects.filter(
            timetable=timetable,
            cycle_day=cycle_day,
            meal__start_time__hour=date.hour,
            meal__start_time__minute=date.minute
        )

        kwargs = {
            'timetable': timetable,
            'vendor': vendor,
            'date': date
        }
        if not cls.objects.filter(**kwargs).exists():
            cls.run_update(timetable, vendor, date, menu_items)

        servings = []
        for menu_item in menu_items:
            serving = Serving.objects.get(
                menu_item=menu_item,
                vendor=vendor,
                date_served=date
            )
            servings.append(serving)

        return servings

    @classmethod
    def run_update(cls, timetable, vendor, date, menu_items):
        for menu_item in menu_items:
            try:
                Serving.objects.create(
                    menu_item=menu_item,
                    vendor=vendor,
                    date_served=date
                )
            except IntegrityError:
                pass

        if menu_items:
            cls.objects.create(
                timetable=timetable,
                vendor=vendor,
                date=date
            )

    def __str__(self):
        return '{} - {} - {}'.format(self.timetable, self.vendor, self.date)

    class Meta:
        unique_together = ('timetable', 'vendor', 'date')
