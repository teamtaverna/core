from django.contrib import admin

from .models import (
    Event, Weekday, Course, Meal, Timetable, Dish, MenuItem,
    Vendor, Serving, TimetableManagement
)


@admin.register(Weekday)
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


class WeekdaysInline(admin.TabularInline):
    """Tabular inline setting for Timetable inactive weekdays."""

    model = Timetable.inactive_weekdays.through


class VendorsInline(admin.TabularInline):
    """Tabular inline setting for Timetable vendors."""

    model = Timetable.vendor.through


@admin.register(Timetable)
class TimetableAdmin(admin.ModelAdmin):
    """Admin customisation for Timetable model."""

    readonly_fields = ('slug', 'date_created', 'date_modified')
    fields = (
        'name', 'slug', 'code', 'api_key', 'cycle_length',
        'current_cycle_day', 'description', 'is_active',
        'cycle_day_updated', 'date_created', 'date_modified'
    )
    inlines = (WeekdaysInline, AdminsInline, VendorsInline)


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    """Admin customisation for Dish model."""

    readonly_fields = ('slug', 'date_created', 'date_modified')
    fields = ('name', 'slug', 'description', 'date_created', 'date_modified')


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    """Admin customisation for MenuItem model."""

    readonly_fields = ('public_id', 'date_created', 'date_modified')
    fields = (
        'public_id', 'timetable', 'cycle_day', 'meal',
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

    fields = ('name', 'slug', 'info', 'start_date', 'end_date')


@admin.register(Serving)
class ServingAdmin(TimeStampAdmin):
    """Admin customisation for Serving model."""

    fields = ('menu_item', 'date_served')


admin.site.empty_value_display = ''

admin.site.register(TimetableManagement)
