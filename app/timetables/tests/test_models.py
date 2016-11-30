from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.test import TestCase
from django.utils import timezone

from app.timetables.factories import (
    CourseFactory, DishFactory, EventFactory, MealFactory, MenuItemFactory,
    ServingFactory, TimetableFactory, VendorFactory, VendorServiceFactory,
    WeekdayFactory
)

from app.timetables.models import (
    Course, Dish, Event, Meal, MenuItem, Serving, Timetable, Vendor,
    VendorService, Weekday
)


class WeekdayTest(TestCase):
    """Tests the Weekday model."""

    def setUp(self):
        WeekdayFactory()

    def test_duplicate_weekday_name_cannot_be_saved(self):
        day = Weekday(name='Monday')

        self.assertRaises(ValidationError, day.save)


class MealTest(TestCase):
    """Tests the Meal model."""

    def setUp(self):
        self.meal = MealFactory()

    def test_duplicate_meal_name_cannot_be_saved(self):
        meal = Meal(
            name='breakfast',
            start_time=self.meal.start_time,
            end_time=self.meal.end_time
        )

        self.assertRaises(ValidationError, meal.save)

    def test_meal_end_time_less_than_start_time_cannot_be_saved(self):
        meal = Meal(
            name='lunch',
            start_time=self.meal.end_time,
            end_time=self.meal.start_time
        )

        self.assertRaises(ValidationError, meal.save)

    def test_meal_end_time_same_with_start_time_cannot_be_saved(self):
        meal = Meal(
            name='lunch',
            start_time=self.meal.start_time,
            end_time=self.meal.start_time
        )

        self.assertRaises(ValidationError, meal.save)


class CourseTest(TestCase):
    """Tests the Course model."""

    def setUp(self):
        CourseFactory()

    def test_duplicate_course_name_cannot_be_saved(self):
        course = Course(
            name='appetizer',
            sequence_order=2
        )

        self.assertRaises(ValidationError, course.save)


class TimetableTest(TestCase):
    """Tests the Timetable model."""

    def setUp(self):
        self.timetable = TimetableFactory()
        self.another_timetable = Timetable(
            name='timetable',
            code='FT7871',
            api_key='TF78993jTA',
            cycle_length=self.timetable.cycle_length,
            ref_cycle_day=self.timetable.ref_cycle_day,
            ref_cycle_date=self.timetable.ref_cycle_date,
            description=self.timetable.description
        )

    def test_duplicate_timetable_name_cannot_be_saved(self):
        self.another_timetable.name = 'fellows timetable'

        self.assertRaises(ValidationError, self.another_timetable.save)

    def test_duplicate_timetable_code_cannot_be_saved(self):
        self.another_timetable.code = self.timetable.code

        self.assertRaises(ValidationError, self.another_timetable.save)

    def test_duplicate_api_key_cannot_be_saved(self):
        self.another_timetable.api_key = self.timetable.api_key

        self.assertRaises(ValidationError, self.another_timetable.save)

    def test_ref_cycle_day_greater_than_cycle_length_cannot_be_saved(self):
        self.another_timetable.ref_cycle_day = self.timetable.cycle_length + 1

        self.assertRaises(ValidationError, self.another_timetable.save)

    def test_cycle_length_and_ref_cycle_day_of_zero_cant_be_saved(self):
        # test for cycle_length == 0
        self.another_timetable.cycle_length = 0
        self.assertRaises(ValidationError, self.another_timetable.save)

        # test for ref_cycle_day == 0
        self.another_timetable.ref_cycle_day = 0
        self.another_timetable.cycle_length = self.timetable.cycle_length

        self.assertRaises(ValidationError, self.another_timetable.save)

    def test_cycle_length_and_ref_cycle_day_of_negative_value_cant_be_saved(self):
        # test for cycle_length < 0
        self.another_timetable.cycle_length = -3
        self.assertRaises(ValidationError, self.another_timetable.save)

        # test for ref_cycle_day < 0
        self.another_timetable.ref_cycle_day = -3
        self.another_timetable.cycle_length = self.timetable.cycle_length

        self.assertRaises(ValidationError, self.another_timetable.save)

    def test_calculate_cycle_day(self):
        test_date = timezone.make_aware(timezone.datetime(2016, 11, 23, 12, 30, 0))
        self.assertEqual(13, self.timetable.calculate_cycle_day(test_date))

        test_date = timezone.make_aware(timezone.datetime(2016, 11, 24, 12, 30, 0))
        self.assertEqual(14, self.timetable.calculate_cycle_day(test_date))

        test_date = timezone.make_aware(timezone.datetime(2016, 11, 25, 12, 30, 0))
        self.assertEqual(1, self.timetable.calculate_cycle_day(test_date))

        test_date = timezone.make_aware(timezone.datetime(2016, 9, 25, 12, 30, 0))
        self.assertEqual(None, self.timetable.calculate_cycle_day(test_date))

    def test_get_vendors(self):
        vendor_service = VendorServiceFactory(timetable=self.timetable)

        new_vendors = [VendorFactory(name=x) for x in ['Spicy Foods', 'Tantalizer']]
        start_date = timezone.make_aware(timezone.datetime(2016, 10, 1, 0, 0, 0))
        end_date = timezone.make_aware(timezone.datetime(2016, 11, 30, 0, 0, 0))

        for new_vendor in new_vendors:
            VendorServiceFactory(
                timetable=self.timetable,
                vendor=new_vendor,
                start_date=start_date,
                end_date=end_date
            )

        test_date = timezone.make_aware(timezone.datetime(2016, 11, 25, 12, 30, 0))
        self.assertEqual(new_vendors, self.timetable.get_vendors(test_date))

        test_date = timezone.make_aware(timezone.datetime(2008, 2, 23, 0, 0, 0))
        self.assertEqual([vendor_service.vendor], self.timetable.get_vendors(test_date))

        test_date = timezone.make_aware(timezone.datetime(2000, 2, 23, 0, 0, 0))
        self.assertEqual([], self.timetable.get_vendors(test_date))


class DishTest(TestCase):
    """Tests the Dish model."""

    def setUp(self):
        self.dish = DishFactory()

    def test_duplicate_dish_name_cannot_be_saved(self):
        dish = Dish(
            name='Coconut Rice',
            description=self.dish.description
        )

        self.assertRaises(ValidationError, dish.save)


class MenuItemTest(TestCase):
    """Tests the MenuItem model."""

    def setUp(self):
        self.menu_item = MenuItemFactory()
        self.another_menu_item = MenuItem(
            timetable=self.menu_item.timetable,
            cycle_day=self.menu_item.cycle_day,
            meal=self.menu_item.meal,
            course=self.menu_item.course,
            dish=self.menu_item.dish
        )

    def test_duplicates_of_all_cannot_be_saved(self):
        self.assertRaises(ValidationError, self.another_menu_item.save)

    def test_zero_cycle_day_value_cannot_be_saved(self):
        self.another_menu_item.cycle_day = 0

        self.assertRaises(ValidationError, self.another_menu_item.save)


class EventTest(TestCase):
    """Tests the Event model."""

    def setUp(self):
        self.event = EventFactory()
        self.another_event = Event(
            name=self.event.name,
            timetable=self.event.timetable,
            action=self.event.action,
            start_date=self.event.start_date,
            end_date=self.event.end_date
        )

    def test_event_uniqueness(self):
        self.assertRaises(IntegrityError, self.another_event.save)

    def test_event_end_time_less_than_start_time_cannot_be_saved(self):
        self.another_event.start_date = self.event.end_date
        self.another_event.end_date = self.event.start_date

        self.assertRaises(ValidationError, self.another_event.save)

    def test_event_end_time_same_with_start_time_cannot_be_saved(self):
        self.another_event.end_date = self.event.start_date

        self.assertRaises(ValidationError, self.another_event.save)


class VendorTest(TestCase):
    """Test the Vendor model."""

    def setUp(self):
        self.vendor = VendorFactory()
        self.another_vendor = Vendor(
            name='mama Taverna'
        )

    def test_enforcement_of_uniqueness_of_vendor_name(self):
        self.assertRaises(ValidationError, self.another_vendor.save)


class ServingTest(TestCase):
    """Test the Serving model."""

    def setUp(self):
        self.serving = ServingFactory()
        self.another_serving = Serving(
            menu_item=self.serving.menu_item,
            vendor=self.serving.vendor,
            date_served=self.serving.date_served
        )

    def test_enforcement_of_unique_together(self):
        self.assertRaises(IntegrityError, self.another_serving.save)


class VendorServiceTest(TestCase):
    """Test the VendorService model"""

    def setUp(self):
        self.vendor_service = VendorServiceFactory()
        self.another_vendor_service = VendorService(
            timetable=self.vendor_service.timetable,
            vendor=self.vendor_service.vendor
        )

    def test_enforcement_of_uniqueness_of_timetable_and_vendor_together(self):
        self.assertRaises(ValidationError, self.another_vendor_service.save)

    def test_enforcement_of_vendor_service_start_date_being_less_than_its_end_date(self):
        self.another_vendor_service.vendor = VendorFactory(name='Papa Taverna')

        # test for start_date == end_date
        self.another_vendor_service.start_date = self.vendor_service.start_date
        self.another_vendor_service.end_date = self.vendor_service.start_date
        self.assertRaises(ValidationError, self.another_vendor_service.save)

        # test for start_date > end_date
        self.another_vendor_service.start_date = self.vendor_service.end_date
        self.assertRaises(ValidationError, self.another_vendor_service.save)
