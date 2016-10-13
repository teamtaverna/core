from datetime import datetime

from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.test import TestCase
from django.utils import timezone

from app.timetables.models import (
    Event, Weekday, Meal, MealOption, Course, Timetable, Dish, MenuItem, Vendor
)

from app.timetables.factories import WeekdayFactory


class WeekdayTest(TestCase):
    """Tests the Weekday model."""

    def setUp(self):
        WeekdayFactory.create()

    def test_duplicate_weekday_name_cannot_be_saved(self):
        day = Weekday(name='Monday')

        self.assertRaises(ValidationError, day.save)


class MealTest(TestCase):
    """Tests the Meal model."""

    def setUp(self):
        Meal.objects.create(
            name='Breakfast',
            start_time=datetime.time(datetime.strptime('5:7:9', '%H:%M:%S')),
            end_time=datetime.time(datetime.strptime('6:7:9', '%H:%M:%S'))
        )

    def test_duplicate_meal_name_cannot_be_saved(self):
        meal = Meal(
            name='breakfast',
            start_time=datetime.time(datetime.strptime('5:7:9', '%H:%M:%S')),
            end_time=datetime.time(datetime.strptime('6:7:9', '%H:%M:%S'))
        )

        self.assertRaises(ValidationError, meal.save)

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
        MealOption.objects.create(name='Lunch')

    def test_duplicate_mealoption_cannot_be_saved(self):
        option = MealOption(name='lunch')

        self.assertRaises(ValidationError, option.save)


class CourseTest(TestCase):
    """Tests the Course model."""

    def setUp(self):
        Course.objects.create(name='test')

    def test_duplicate_course_name_cannot_be_saved(self):
        course = Course(name='Test')

        self.assertRaises(ValidationError, course.save)


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
        dish = Dish(name='Eba')

        self.assertRaises(ValidationError, dish.save)


class MenuItemTest(TestCase):
    """Tests the MenuItem model."""

    def setUp(self):
        self.timetable_object = Timetable.objects.create(
            name='timtable-item',
            code='FBI23212',
            api_key='419223',
            cycle_length=14,
            current_cycle_day=2,
            date_created=datetime.strptime('05 07 2016', '%d %m %Y'),
            date_modified=datetime.strptime('06 08 2016', '%d %m %Y')
        )

        self.meal_object = Meal.objects.create(
            name='breakfast',
            start_time=datetime.time(datetime.strptime('5:7:9', '%H:%M:%S')),
            end_time=datetime.time(datetime.strptime('6:7:9', '%H:%M:%S'))
        )

        self.meal_option = MealOption.objects.create(name='lunch')

        self.menu_item_object = {
            'timetable': self.timetable_object,
            'cycle_day': 4,
            'meal': self.meal_object,
            'meal_option': self.meal_option
        }

        MenuItem.objects.create(**self.menu_item_object)

    def test_duplicates_of_all_cannot_be_saved(self):
        menu_item_two = MenuItem(**self.menu_item_object)

        self.assertRaises(ValidationError, menu_item_two.save)

    def test_zero_cycle_day_value_cannot_be_saved(self):
        menu_item_three = MenuItem(
            cycle_day=0,
            meal=self.meal_object,
            meal_option=self.meal_option,
            timetable=self.timetable_object)

        self.assertRaises(ValidationError, menu_item_three.save)


class EventTest(TestCase):
    """Tests the Event model."""

    def setUp(self):
        self.future_date = datetime.strptime('07 08 2016 05 30', '%d %m %Y %H %M')
        self.earlier_date = datetime.strptime('06 07 2016 05 30', '%d %m %Y %H %M')
        self.timetable = Timetable.objects.create(
            name='timtable-item',
            code='FBI23212',
            api_key='419223',
            cycle_length=14,
            current_cycle_day=2,
            date_created=self.earlier_date,
            date_modified=self.future_date
        )
        self.event_data = {
            'name': 'some event',
            'timetable': self.timetable,
            'start_date': self.earlier_date,
            'end_date': self.future_date,
        }
        Event.objects.create(**self.event_data)

    def test_event_was_created(self):
        event = Event.objects.get(timetable=self.timetable)

        self.assertEqual(event.timetable.id, self.timetable.id)

    def test_event_end_time_less_than_start_time_cannot_be_saved(self):
        event = Event(
            name='Special',
            timetable=self.timetable,
            start_date=self.future_date,
            end_date=self.earlier_date
        )

        self.assertRaises(ValidationError, event.save)

    def test_event_end_time_same_with_start_time_cannot_be_saved(self):
        event = Event(
            name='Special',
            timetable=self.timetable,
            start_date=self.earlier_date,
            end_date=self.earlier_date
        )

        self.assertRaises(ValidationError, event.save)

    def test_event_uniqueness(self):
        event = Event(**self.event_data)

        self.assertRaises(IntegrityError, event.save)


class VendorTest(TestCase):
    """Test the Vendor model."""

    def setUp(self):
        Vendor.objects.create(
            name='Spicy Foods',
            info='Reach us at info@spicy-foods.com',
            start_date=timezone.make_aware(timezone.datetime(2016, 7, 5, 13, 0, 0)),
            end_date=timezone.make_aware(timezone.datetime(2017, 7, 5, 13, 0, 0))
        )

    def test_enforcement_of_uniqueness_of_vendor_name(self):
        vendor = Vendor(
            name='spicy foods',
            start_date=timezone.make_aware(timezone.datetime(2016, 8, 5, 13, 0, 0)),
            end_date=timezone.make_aware(timezone.datetime(2017, 8, 5, 13, 0, 0))
        )

        self.assertRaises(ValidationError, vendor.save)

    def test_enforcement_of_vendor_start_date_being_less_than_its_end_date(self):
        # test for start_date == end_date
        vendor = Vendor(
            name='Fresh Foods',
            start_date=timezone.make_aware(timezone.datetime(2016, 8, 5, 13, 0, 0)),
            end_date=timezone.make_aware(timezone.datetime(2016, 8, 5, 13, 0, 0))
        )
        self.assertRaises(ValidationError, vendor.save)

        # test for start_date >= end_date
        vendor.end_date = timezone.make_aware(timezone.datetime(2015, 8, 5, 13, 0, 0))
        self.assertRaises(ValidationError, vendor.save)
