from django.contrib import admin

from . import models


class WeekdayAdmin(admin.ModelAdmin):
    readonly_fields = ('slug',)
    empty_value_display = ''

admin.site.register(models.Weekday, WeekdayAdmin)
admin.site.register(models.Meal)
admin.site.register(models.MealOption)
admin.site.register(models.Course)
admin.site.register(models.Timetable)
admin.site.register(models.Dish)
admin.site.register(models.Admin)
admin.site.register(models.MenuItem)
