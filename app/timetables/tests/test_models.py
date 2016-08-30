from datetime import datetime

from django.test import TestCase
from django.db import IntegrityError
from django.core.exceptions import ValidationError

from app.timetables.models import Weekday, Meal, MealOption


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
            start_time=datetime.time(datetime.strptime('5:7:9', '%H:%M:%S')),
            end_time=datetime.time(datetime.strptime('6:7:9', '%H:%M:%S'))
        )

    def test_meal_name_should_be_capitalized_on_save(self):
        meal = Meal.objects.get(name__iexact="breakfast")

        self.assertEqual(meal.name, 'Breakfast')

    def test_duplicate_meal_name_cannot_be_saved(self):
        meal = Meal(
            name='Breakfast',
            start_time=datetime.time(datetime.strptime('5:7:9', '%H:%M:%S')),
            end_time=datetime.time(datetime.strptime('6:7:9', '%H:%M:%S'))
        )

        self.assertRaises(IntegrityError, meal.save)

    def test_meal_end_time_less_than_start_time_cannot_be_saved(self):
        meal = Meal(
            name='lunch',
            start_time=datetime.time(datetime.strptime('10:7:9', '%H:%M:%S')),
            end_time=datetime.time(datetime.strptime('9:7:9', '%H:%M:%S'))
        )

        self.assertRaises(ValidationError, meal.save)

    def test_meal_end_time_same_with_start_time_cannot_be_saved(self):
        meal = Meal(
            name='lunch',
            start_time=datetime.time(datetime.strptime('10:7:9', '%H:%M:%S')),
            end_time=datetime.time(datetime.strptime('10:7:9', '%H:%M:%S'))
        )

        self.assertRaises(ValidationError, meal.save)


class MealOptionTest(TestCase):
    """Tests the MealOption model."""

    def setUp(self):
        MealOption.objects.create(name='lunch')

    def test_mealoption_name_should_be_capitalized_on_save(self):
        option = MealOption.objects.get(name__iexact='lunch')

        self.assertEqual(option.name, 'Lunch')

    def test_duplicate_mealoption_name_cannot_be_saved(self):
        option = MealOption(name='lunch')

        self.assertRaises(IntegrityError, option.save)
