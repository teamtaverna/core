from datetime import datetime

from django.test import TestCase
from django.db import IntegrityError

from app.timetables.models import Weekday, Meal


class WeekdayTest(TestCase):
    """Tests the Weekday model."""

    def setUp(self):
        Weekday.objects.create(name='monday')

    def test_weekday_name_should_be_capitalized_on_save(self):
        day = Weekday.objects.get(name__iexact='monday')

        self.assertEqual(day.name, 'Monday')

    def test_duplicate_weekday_name_cannot_be_saved(self):
        day = Weekday(name='Monday')

        self.assertRaises(IntegrityError, day.save)


class MealTest(TestCase):
    """Tests the Meal model."""

    def setUp(self):
        Meal.objects.create(
            name='breakfast',
            start_time=datetime.strptime('21:30:05', '%H:%M:%S').time(),
            end_time=datetime.strptime('22:30:05', '%H:%M:%S').time()
        )

    def test_meal_name_should_be_capitalized_on_save(self):
        meal = Meal.objects.get(name__iexact="breakfast")

        self.assertEqual(meal.name, 'Breakfast')

    def test_duplicate_meal_name_cannot_be_saved(self):
        meal = Meal(name='Breakfast')

        self.assertRaises(IntegrityError, meal.save)
