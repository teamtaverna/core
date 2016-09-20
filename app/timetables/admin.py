from django.contrib import admin

from . import models


@admin.register(models.Weekday, models.MealOption, models.Course)
class DefaultAdmin(admin.ModelAdmin):
    """Default admin for models with just name and slug fields."""
    readonly_fields = ('slug',)


@admin.register(models.Meal)
class MealAdmin(DefaultAdmin):
    fields = ('name', 'slug', 'start_time', 'end_time')


class AdminsInline(admin.TabularInline):
    model = models.Timetable.admins.through


@admin.register(models.Timetable)
class TimetableAdmin(DefaultAdmin):
    fields = ('name', 'slug', 'code', 'api_key', 'cycle_length',
              'current_cycle_day', 'description')
    inlines = (AdminsInline,)


@admin.register(models.Dish)
class DishAdmin(DefaultAdmin):
    fields = ('name', 'slug', 'description')


admin.site.empty_value_display = ''

other_models = [models.Admin, models.MenuItem]
admin.site.register(other_models)
