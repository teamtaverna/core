from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import (MinValueValidator,
                                    validate_comma_separated_integer_list,)
from django.db import models, transaction
from django.db.utils import IntegrityError
from django.utils.translation import ugettext_lazy as _

from hashid_field import HashidField

from common.mixins import SlugifyMixin, TimestampMixin
from common.utils import timestamp_seconds


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
    """
    Model representing the sequence/order of different kind
    of dishes for a meal."""

    name = models.CharField(
        max_length=150, help_text='Example: appetizer, main course, dessert'
    )
    slug = models.SlugField(
        max_length=150, unique=True, null=True, editable=False
    )
    sequence_order = models.PositiveSmallIntegerField(
        unique=True,
        help_text=(
            'The numerical order of the dishes for a meal option. '
            'E.g, 1 for appetizer, 2 for main course'
        )
    )

    slugify_field = 'name'

    def __str__(self):
        return self.name


class Vendor(SlugifyMixin, models.Model):
    """Model representing food service-provider."""

    name = models.CharField(max_length=255, verbose_name="Vendor Name")
    slug = models.SlugField(max_length=255, unique=True, editable=False)
    info = models.TextField(blank=True)

    slugify_field = 'name'

    def is_vendor_serving(self, timetable, date):
        query = (models.Q(timetable=timetable, vendor=self, end_date__gte=date)
                 | models.Q(timetable=timetable, vendor=self, end_date=None))
        return VendorService.objects.filter(query).exists()

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
    cycle_length = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)],
        help_text=(
            'Number of days in which the menu timetable is repeated '
            'after a period of time. E.g, A cycle length of '
            '14 days (2 weeks) including the inactive weekdays '
            'like weekends after which the food schedule is repeated.'
        )
    )
    ref_cycle_day = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)],
        help_text=(
            'The reference day (numerical value) in time '
            'with which cycle day for any other following date '
            'can be computed. E.g, 1 if today is Sunday as '
            'first day of the cycle length. No need to always '
            'update this except the cycle changes.'
        )
    )
    ref_cycle_date = models.DateField(
        help_text=(
            'The reference date in time with which cycle day '
            'for any other following date can be computed. '
            'E.g, 1 if today is Sunday as first day of the '
            'cycle length. No need to always '
            'update this except the cycle changes.'
        )
    )
    inactive_weekdays = models.CharField(
        max_length=13,  # At max., we would have '0,1,2,3,4,5,6'
        blank=True,
        validators=[validate_comma_separated_integer_list]
    )
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

    def calculate_cycle_day(self, date):
        days_interval = (date - self.ref_cycle_date).days

        if days_interval < 0:
            raise ValidationError(
                _('Supply a date later than or equal to {}'.format(self.ref_cycle_date))
            )

        cycle_day = (((days_interval % self.cycle_length) + self.ref_cycle_day)
                     % self.cycle_length)

        if cycle_day == 0:
            cycle_day = self.cycle_length

        return cycle_day

    def get_vendors(self, date):
        return [vendor for vendor in Vendor.objects.filter(
            timetable__slug=self.slug,
            vendorservice__start_date__lte=date,
            vendorservice__end_date__gte=date
        )]

    def is_timetable_inactive_this_day(self, date):
        return str(date.weekday()) in self.inactive_weekdays


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
        verbose_name = 'Timetable Admin'
        verbose_name_plural = 'Timetable Admins'


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

    def clean(self):
        if self.cycle_day and self.timetable.cycle_length:
            if self.cycle_day > self.timetable.cycle_length:
                raise ValidationError(
                    _('Supply a cycle day in the range 1 - {}'.format(self.timetable.cycle_length))
                )
        super().clean()

    def save(self, *args, **kwargs):
        # Calling full_clean instead of clean to ensure validators are called
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return '{} ({}) for {} on cycle {} timetable {}'.format(
            self.dish, self.course, self.meal, self.cycle_day, self.timetable
        )

    class Meta:
        unique_together = ('timetable', 'cycle_day', 'meal', 'course', 'dish')
        verbose_name = 'Menu Item'
        verbose_name_plural = 'Menu Items'


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
    date_served = models.DateField()

    def __str__(self):
        return '{} served on {}'.format(self.menu_item, self.date_served)

    class Meta:
        unique_together = ('menu_item', 'vendor', 'date_served')


class VendorService(models.Model):
    """Model representing tenure a vendor serves a specific timetable."""

    timetable = models.ForeignKey(Timetable, on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    start_date = models.DateField(default=None, null=True, blank=True)
    end_date = models.DateField(default=None, null=True, blank=True)

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
        verbose_name = 'Vendor Service'
        verbose_name_plural = 'Vendor Services'


class ServingAutoUpdate(models.Model):
    """Model representing Automatic Update of Servings."""

    timetable = models.ForeignKey(Timetable, on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date = models.DateField()

    @staticmethod
    def get_menu_items(timetable, date):
        cycle_day = timetable.calculate_cycle_day(date)
        menu_items = MenuItem.objects.filter(
            timetable=timetable,
            cycle_day=cycle_day
        )

        if not menu_items:
            raise ValidationError(
                _('No matching menu_item for this Timetable and Date combination.')
            )

        return menu_items

    @staticmethod
    def verify_vendor_is_serving(timetable, vendor, date):
        if not vendor.is_vendor_serving(timetable, date):
            raise ValidationError(
                _('Ensure the specified Vendor has an active tenure '
                  'for the specified Date on the specified Timetable')
            )

    @classmethod
    def get_servings(cls, timetable, date, vendor=None):
        if not timetable.is_active or timetable.is_timetable_inactive_this_day(date):
            raise ValidationError(
                _('Timetable {} is inactive on {}.'.format(
                    timetable.name,
                    date,
                ))
            )

        if vendor:
            cls.verify_vendor_is_serving(timetable, vendor, date)
            vendors = [vendor]
        else:
            vendors = Vendor.objects.all()

        menu_items = cls.get_menu_items(timetable, date)

        for vendor in vendors:
            kwargs = {
                'timetable': timetable,
                'vendor': vendor,
                'date': date
            }
            if not cls.objects.filter(**kwargs).exists():
                cls.objects.create(**kwargs)

        return Serving.objects.filter(
            menu_item__in=menu_items,
            vendor__in=vendors,
            date_served=date
        )

    @classmethod
    def create_servings_if_not_exist(cls, timetable, vendor, date):
        cls.verify_vendor_is_serving(timetable, vendor, date)
        menu_items = cls.get_menu_items(timetable, date)

        for menu_item in menu_items:
            try:
                with transaction.atomic():
                    Serving.objects.create(
                        menu_item=menu_item,
                        vendor=vendor,
                        date_served=date
                    )
            except IntegrityError:
                pass

    def clean(self):
        # This is called here instead of save() in order to handle ValidationError
        self.create_servings_if_not_exist(self.timetable, self.vendor, self.date)

    def save(self, *args, **kwargs):
        self.full_clean()

        return super().save(*args, **kwargs)

    def __str__(self):
        return '{} - {} - {}'.format(self.timetable, self.vendor, self.date)

    class Meta:
        unique_together = ('timetable', 'vendor', 'date')
        verbose_name = 'ServingAutoUpdate'
        verbose_name_plural = 'ServingAutoUpdates'
