from django.contrib import admin

from .models import (
    Event, Weekday, MealOption, Course, Meal, Timetable, Dish, Admin, MenuItem,
    Vendor, Serving
)


@admin.register(Weekday, MealOption, Course)
class DefaultAdmin(admin.ModelAdmin):
    """Default admin for models with just name and slug fields."""

    readonly_fields = ('slug',)


class TimeStampAdmin(admin.ModelAdmin):
    """Default admin for models having only readonly fields from TimeStampMixin."""

    readonly_fields = ('date_created', 'date_modified')


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


@admin.register(Timetable)
class TimetableAdmin(admin.ModelAdmin):
    """Admin customisation for Timetable model."""

    readonly_fields = ('slug', 'date_created', 'date_modified')
    fields = ('name', 'slug', 'code', 'api_key', 'cycle_length',
              'current_cycle_day', 'description', 'date_created',
              'date_modified')
    inlines = (WeekdaysInline, AdminsInline,)


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    """Admin customisation for Dish model."""

    readonly_fields = ('slug', 'date_created', 'date_modified')
    fields = ('name', 'slug', 'description', 'date_created', 'date_modified')


@admin.register(MenuItem)
class MenuItemAdmin(TimeStampAdmin):
    """Admin customisation for MenuItem model."""

    fields = ('timetable', 'cycle_day', 'meal', 'meal_option', 'date_created',
              'date_modified')


@admin.register(Event)
class EventAdmin(TimeStampAdmin):
    """Admin customisation for Event model."""

    fields = ('name', 'timetable', 'start_date', 'end_date', 'date_created',
              'date_modified')


@admin.register(Vendor)
class VendorAdmin(DefaultAdmin):
    fields = ('name', 'slug', 'info', 'start_date', 'end_date')


@admin.register(Serving)
class ServingAdmin(TimeStampAdmin):
    """Admin customisation for Serving model."""
    fields = ('menu_item', 'date_served')


admin.site.empty_value_display = ''

other_models = [Admin]
admin.site.register(other_models)
