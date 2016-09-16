from django.contrib import admin

from . import models


admin.site.register(models.Weekday)
admin.site.register(models.Meal)
admin.site.register(models.MealOption)
admin.site.register(models.Course)
admin.site.register(models.Timetable)
admin.site.register(models.Dish)
admin.site.register(models.Admin)
