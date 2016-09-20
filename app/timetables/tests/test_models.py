from datetime import datetime

from django.core.exceptions import ValidationError
from django.test import TestCase

from app.timetables import models


class WeekdayTest(TestCase):
    """Tests the Weekday model."""

    def setUp(self):
        models.Weekday.objects.create(name='monday')

    def test_duplicate_weekday_name_cannot_be_saved(self):
        day = models.Weekday(name='Monday')

        self.assertRaises(ValidationError, day.save)


class MealTest(TestCase):
    """Tests the Meal model."""

    def setUp(self):
        models.Meal.objects.create(
            name='Breakfast',
            start_time=datetime.time(datetime.strptime('5:7:9', '%H:%M:%S')),
            end_time=datetime.time(datetime.strptime('6:7:9', '%H:%M:%S'))
        )

    def test_duplicate_meal_name_cannot_be_saved(self):
        meal = models.Meal(
            name='breakfast',
            start_time=datetime.time(datetime.strptime('5:7:9', '%H:%M:%S')),
            end_time=datetime.time(datetime.strptime('6:7:9', '%H:%M:%S'))
        )

        self.assertRaises(ValidationError, meal.save)

    def test_meal_end_time_less_than_start_time_cannot_be_saved(self):
        meal = models.Meal(
            name='lunch',
            start_time=datetime.time(datetime.strptime('10:7:9', '%H:%M:%S')),
            end_time=datetime.time(datetime.strptime('9:7:9', '%H:%M:%S'))
        )

        self.assertRaises(ValidationError, meal.save)

    def test_meal_end_time_same_with_start_time_cannot_be_saved(self):
        meal = models.Meal(
            name='lunch',
            start_time=datetime.time(datetime.strptime('10:7:9', '%H:%M:%S')),
            end_time=datetime.time(datetime.strptime('10:7:9', '%H:%M:%S'))
        )

        self.assertRaises(ValidationError, meal.save)


class MealOptionTest(TestCase):
    """Tests the MealOption model."""

    def setUp(self):
        models.MealOption.objects.create(name='Lunch')

    def test_duplicate_mealoption_cannot_be_saved(self):
        option = models.MealOption(name='lunch')

        self.assertRaises(ValidationError, option.save)


class CourseTest(TestCase):
    """Tests the Course model."""

    def setUp(self):
        models.Course.objects.create(name='test')

    def test_duplicate_course_name_cannot_be_saved(self):
        course = models.Course(name='Test')

        self.assertRaises(ValidationError, course.save)


class TimetableTest(TestCase):
    """Tests the Timetable model."""

    def setUp(self):
        models.Timetable.objects.create(
            name='timtable-item',
            code='FBI23212',
            api_key='419223',
            cycle_length=14,
            current_cycle_day=2,
            date_created=datetime.strptime('05 07 2016', '%d %m %Y'),
            date_modified=datetime.strptime('06 08 2016', '%d %m %Y')
        )

    def test_duplicate_timetable_name_cannot_be_saved(self):
        timetable = models.Timetable(
            name='timtable-Item',
            code='FB23212',
            api_key='41923',
            cycle_length=14,
            current_cycle_day=2,
            date_created=datetime.strptime('05 07 2016', '%d %m %Y'),
            date_modified=datetime.strptime('06 08 2016', '%d %m %Y')
        )

        self.assertRaises(ValidationError, timetable.save)

    def test_duplicate_timetable_code_cannot_be_saved(self):
        timetable = models.Timetable(
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
        timetable = models.Timetable(
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
        timetable = models.Timetable(
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
        timetable = models.Timetable(
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
        timetable = models.Timetable(
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
        models.Dish.objects.create(
            name='eba',
            description='eba and garri. Make eba for your wedding day.',
            date_created=datetime.strptime('05 07 2016', '%d %m %Y'),
            date_modified=datetime.strptime('06 08 2016', '%d %m %Y')
        )

    def test_duplicate_dish_name_cannot_be_saved(self):
        dish = models.Dish(name='Eba')

        self.assertRaises(ValidationError, dish.save)


class MenuItemTest(TestCase):
    """Tests the MenuItem model."""

    def setUp(self):
        self.timetable_object = models.Timetable.objects.create(
            name='timtable-item',
            code='FBI23212',
            api_key='419223',
            cycle_length=14,
            current_cycle_day=2,
            date_created=datetime.strptime('05 07 2016', '%d %m %Y'),
            date_modified=datetime.strptime('06 08 2016', '%d %m %Y')
        )

        self.meal_object = models.Meal.objects.create(
            name='breakfast',
            start_time=datetime.time(datetime.strptime('5:7:9', '%H:%M:%S')),
            end_time=datetime.time(datetime.strptime('6:7:9', '%H:%M:%S'))
        )

        self.meal_option = models.MealOption.objects.create(name='lunch')

        self.menu_item_object = {
            'timetable': self.timetable_object,
            'cycle_day': 4,
            'meal': self.meal_object,
            'meal_option': self.meal_option
        }

        models.MenuItem.objects.create(**self.menu_item_object)

    def test_duplicates_of_all_cannot_be_saved(self):
        menu_item_two = models.MenuItem(**self.menu_item_object)

        self.assertRaises(ValidationError, menu_item_two.save)

    def test_zero_cycle_day_value_cannot_be_saved(self):
        menu_item_three = models.MenuItem(
            cycle_day=0,
            meal=self.meal_object,
            meal_option=self.meal_option,
            timetable=self.timetable_object)

        self.assertRaises(ValidationError, menu_item_three.save)
