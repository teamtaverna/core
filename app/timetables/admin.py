from django.contrib import admin

from .models import Course, Meal, MealOption, Weekday, Timetable, Dish


admin.site.register(Weekday)
admin.site.register(Meal)
admin.site.register(MealOption)
admin.site.register(Course)
admin.site.register(Timetable)
admin.site.register(Dish)
