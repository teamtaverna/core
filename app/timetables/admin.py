from django.contrib import admin

<<<<<<< 30a887456af0307c996224767574a2cb23e50764
from .models import Weekday, Meal, MealOption
=======
from .models import Weekday, MealOption
>>>>>>> Remove unneccessary inheritance and correct spacing


admin.site.register(Weekday)
admin.site.register(Meal)
admin.site.register(MealOption)
