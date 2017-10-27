from django import forms
from django.conf import settings
from django.contrib import admin

from .models import (
    Course, Dish, Event, Meal, MenuItem, Serving, ServingAutoUpdate,
    Timetable, TimetableManagement, Vendor, VendorService,
)


def clear_actions(actions):
    [actions.pop(key) for key in actions]


class DefaultAdmin(admin.ModelAdmin):
    """Default admin for models with just name and slug fields."""

    readonly_fields = ('slug',)


class TimeStampAdmin(admin.ModelAdmin):
    """
    Default admin for models having only readonly fields
    from TimeStampMixin.
    """

    readonly_fields = ('date_created', 'date_modified')


@admin.register(Course)
class CourseAdmin(DefaultAdmin):
    """Admin customisation for Course model."""

    fieldsets = [
        ('Course', {
            'fields': ('name', 'slug', 'sequence_order',),
            'description': ('A particular dish served as one '
                            'of the successive parts of a meal option.')
        }),
    ]


@admin.register(Meal)
class MealAdmin(DefaultAdmin):
    """Admin customisation for Meal model."""

    fieldsets = [
        ('Meal', {
            'fields': ('name', 'slug', 'start_time', 'end_time',),
            'description': ('One of the occasions during the day '
                            'that food is scheduled to be served. '
                            'For example breakfast, lunch, tea-break.')
        }),
    ]


class AdminsInline(admin.TabularInline):
    """Tabular inline setting for Timetable admins."""

    model = Timetable.admins.through


class VendorsInline(admin.TabularInline):
    """Tabular inline setting for Timetable vendors."""

    model = Timetable.vendors.through


class TimetableForm(forms.ModelForm):
    inactive_weekdays = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=((key, value) for key, value in enumerate(settings.WEEKDAYS)),
    )

    def __init__(self, *args, **kwargs):
        if kwargs.get('instance'):
            # inactive_weekdays field is a list of integer at the form level
            kwargs['instance'].inactive_weekdays = kwargs['instance'].inactive_weekdays.split(',')
        super().__init__(*args, **kwargs)

    def clean_inactive_weekdays(self):
        # inactive_weekdays field is a string of comma-separated list of integer at the model level
        return ','.join(self.cleaned_data['inactive_weekdays'])


@admin.register(Timetable)
class TimetableAdmin(admin.ModelAdmin):
    """Admin customisation for Timetable model."""

    readonly_fields = ('slug', 'date_created', 'date_modified')
    fieldsets = [
        ('Timetable', {
            'fields': ('name', 'slug', 'cycle_length', 'ref_cycle_day',
                       'description', 'is_active', 'ref_cycle_date',
                       'inactive_weekdays', 'date_created', 'date_modified',),
            'description': ('Holds the entire structure and scheduling of '
                            'meals, menu-items, etc, served at a location, '
                            'to a team or the entire organization.')
        }),
    ]
    form = TimetableForm
    inlines = (AdminsInline, VendorsInline)


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    """Admin customisation for Dish model."""

    readonly_fields = ('slug', 'date_created', 'date_modified')
    search_fields = ('name',)
    fieldsets = [
        ('Dish', {
            'fields': ('name', 'slug', 'description', 'date_created',
                       'date_modified',),
            'description': ('The actual food served as a given course. '
                            'For example, Coconut rice garnished with '
                            'fish stew and chicken or just Ice-cream.')
        }),
    ]


@admin.register(MenuItem)
class MenuItemAdmin(TimeStampAdmin):
    """Admin customisation for MenuItem model."""

    fieldsets = [
        ('Menu Item', {
            'fields': ('timetable', 'cycle_day', 'meal', 'course',
                       'dish', 'date_created', 'date_modified',),
            'description': 'Meal combination option to be served.'
        }),
    ]

    search_fields = (
        'timetable__name',
        'cycle_day',
        'meal__name',
        'course__name',
        'dish__name'
        )

    list_filter = (
        'timetable__name',
        'cycle_day',
        'meal__name',
        'course__name',
        'dish__name'
        )


@admin.register(Event)
class EventAdmin(TimeStampAdmin):
    """Admin customisation for Event model."""

    fieldsets = [
        ('Event', {
            'fields': ('name', 'timetable', 'action', 'start_date', 'end_date',
                       'date_created', 'date_modified',),
            'description': ('A date or range of dates to prevent '
                            'food scheduling or user reviews during that '
                            'period. Example: Christmas.')
        }),
    ]


@admin.register(Vendor)
class VendorAdmin(DefaultAdmin):
    """Admin customisation for Vendor model."""

    fields = ('name', 'slug', 'info')


@admin.register(VendorService)
class VendorServiceAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Vendor Service', {
            'fields': ('timetable', 'vendor', 'start_date', 'end_date',),
            'description': 'The tenure a vendor serves a specific timetable.'
        }),
    ]

admin.site.empty_value_display = ''

admin.site.register(TimetableManagement)
admin.site.register(Serving)
admin.site.register(ServingAutoUpdate)
