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
    """Default admin for models having only readonly fields from TimeStampMixin."""

    readonly_fields = ('date_created', 'date_modified')


@admin.register(Course)
class CourseAdmin(DefaultAdmin):
    """Admin customisation for Course model."""

    fields = ('name', 'slug', 'sequence_order')


@admin.register(Meal)
class MealAdmin(DefaultAdmin):
    """Admin customisation for Meal model."""

    fields = ('name', 'slug', 'start_time', 'end_time')


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
    fields = (
        'name', 'slug', 'cycle_length',
        'ref_cycle_day', 'description', 'is_active',
        'ref_cycle_date', 'inactive_weekdays', 'date_created', 'date_modified'
    )
    form = TimetableForm
    inlines = (AdminsInline, VendorsInline)


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    """Admin customisation for Dish model."""

    readonly_fields = ('slug', 'date_created', 'date_modified')
    fields = ('name', 'slug', 'description', 'date_created', 'date_modified')


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    """Admin customisation for MenuItem model."""

    readonly_fields = ('date_created', 'date_modified')
    fields = (
        'timetable', 'cycle_day', 'meal',
        'course', 'dish', 'date_created', 'date_modified'
    )


@admin.register(Event)
class EventAdmin(TimeStampAdmin):
    """Admin customisation for Event model."""

    fields = (
        'name', 'timetable', 'action', 'start_date', 'end_date',
        'date_created', 'date_modified'
    )


@admin.register(Vendor)
class VendorAdmin(DefaultAdmin):
    """Admin customisation for Vendor model."""

    fields = ('name', 'slug', 'info')


@admin.register(Serving)
class ServingAdmin(TimeStampAdmin):
    """Admin customisation for Serving model."""

    fields = ('public_id', 'menu_item', 'vendor', 'date_served')
    readonly_fields = fields

    def get_actions(self, request):
        actions = super().get_actions(request)
        if not settings.DEBUG:
            clear_actions(actions)

        return actions

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.empty_value_display = ''

admin.site.register([TimetableManagement, VendorService])
if settings.DEBUG:
    admin.site.register(ServingAutoUpdate)
