from datetime import datetime

from django.test import TestCase
from django.db import IntegrityError
from django.core.exceptions import ValidationError

from app.timetables.models import Course, Meal, MealOption, Weekday, Timetable, Dish


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


class CourseTest(TestCase):
    """Tests the Course model."""

    def setUp(self):
        Course.objects.create(name='test')

    def test_course_name_should_be_capitalized_on_save(self):
        course = Course.objects.get(name__iexact='test')

        self.assertEqual(course.name, 'Test')

    def test_duplicate_course_name_cannot_be_saved(self):
        course = Course(name='test')

        self.assertRaises(IntegrityError, course.save)


class TimetableTest(TestCase):
    """Tests the Timetable model."""

    def setUp(self):
        Timetable.objects.create(
            name='timtable-item',
            code='FBI23212',
            api_key='419223',
            cycle_length=14,
            current_cycle_day=2,
            date_created=datetime.strptime('05 07 2016', '%d %m %Y'),
            date_modified=datetime.strptime('06 08 2016', '%d %m %Y')
        )

    def test_duplicate_timetable_name_cannot_be_saved(self):
        timetable = Timetable(
            name='timtable-item',
            code='FB23212',
            api_key='41923',
            cycle_length=14,
            current_cycle_day=2,
            date_created=datetime.strptime('05 07 2016', '%d %m %Y'),
            date_modified=datetime.strptime('06 08 2016', '%d %m %Y')
        )

        self.assertRaises(ValidationError, timetable.save)

    def test_duplicate_timetable_code_cannot_be_saved(self):
        timetable = Timetable(
            name='timtable-value',
            code='FBI23212',
            api_key='41923',
            cycle_length=14,
            current_cycle_day=2,
            date_created=datetime.strptime('05 07 2016', '%d %m %Y'),
            date_modified=datetime.strptime('06 08 2016', '%d %m %Y')
        )

        self.assertRaises(ValidationError, timetable.save)

    def test_duplicate_api_key_cannot_be_saved(self):
        timetable = Timetable(
            name='timtable',
            code='FBI232123',
            api_key='419223',
            cycle_length=14,
            current_cycle_day=2,
            date_created=datetime.strptime('05 07 2016', '%d %m %Y'),
            date_modified=datetime.strptime('06 08 2016', '%d %m %Y')
        )

        self.assertRaises(ValidationError, timetable.save)

    def test_current_cycle_day_greater_than_cycle_length_cannot_be_saved(self):
        timetable = Timetable(
            name='timtable',
            code='FBI232123',
            api_key='4192237',
            cycle_length=1,
            current_cycle_day=2,
            date_created=datetime.strptime('05 07 2016', '%d %m %Y'),
            date_modified=datetime.strptime('06 08 2016', '%d %m %Y')
        )

        self.assertRaises(ValidationError, timetable.save)

    def test_cycle_length_and_current_cycle_day_of_zero_cant_be_saved(self):
        timetable = Timetable(
            name='timtable',
            code='FBI232123',
            api_key='4192237',
            cycle_length=0,
            current_cycle_day=0,
            date_created=datetime.strptime('05 07 2016', '%d %m %Y'),
            date_modified=datetime.strptime('06 08 2016', '%d %m %Y')
        )

        self.assertRaises(ValidationError, timetable.save)

    def test_cycle_length_and_current_cycle_day_of_negative_value_cant_be_saved(self):
        timetable = Timetable(
            name='timtable',
            code='FBI232123',
            api_key='4192237',
            cycle_length=-1,
            current_cycle_day=-3,
            date_created=datetime.strptime('05 07 2016', '%d %m %Y'),
            date_modified=datetime.strptime('06 08 2016', '%d %m %Y')
        )

        self.assertRaises(ValidationError, timetable.save)


class DishTest(TestCase):
    """Tests the Dish model."""

    def setUp(self):
        Dish.objects.create(
            name='eba',
            description='eba and garri. Make eba for your wedding day.',
            date_created=datetime.strptime('05 07 2016', '%d %m %Y'),
            date_modified=datetime.strptime('06 08 2016', '%d %m %Y')
        )

    def test_duplicate_dish_name_cannot_be_saved(self):
        dish = Dish(name='eba')

        self.assertRaises(IntegrityError, dish.save)
