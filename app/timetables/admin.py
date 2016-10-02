from django.contrib import admin

from .models import (
    Event, Weekday, MealOption, Course, Meal, Timetable, Dish, Admin, MenuItem
)


@admin.register(Weekday, MealOption, Course)
class DefaultAdmin(admin.ModelAdmin):
    """Default admin for models with just name and slug fields."""
    readonly_fields = ('slug',)


@admin.register(Meal)
class MealAdmin(DefaultAdmin):
    fields = ('name', 'slug', 'start_time', 'end_time')


class AdminsInline(admin.TabularInline):
    model = Timetable.admins.through


@admin.register(Timetable)
class TimetableAdmin(admin.ModelAdmin):
    readonly_fields = ('slug', 'date_created', 'date_modified')
    fields = ('name', 'slug', 'code', 'api_key', 'cycle_length',
              'current_cycle_day', 'description', 'date_created', 'date_modified')
    inlines = (AdminsInline,)


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    readonly_fields = ('slug', 'date_created', 'date_modified')
    fields = ('name', 'slug', 'description', 'date_created', 'date_modified')


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    readonly_fields = ('date_created', 'date_modified')
    fields = ('timetable', 'cycle_day', 'meal', 'meal_option', 'date_created', 'date_modified')


admin.site.empty_value_display = ''

other_models = [Event, Admin]
admin.site.register(other_models)
