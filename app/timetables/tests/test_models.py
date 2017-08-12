import datetime

from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.utils import IntegrityError
from django.test import TestCase

from app.timetables.factories import (
    CourseFactory, DishFactory, EventFactory, MealFactory, MenuItemFactory,
    ServingFactory, TimetableFactory, VendorFactory, VendorServiceFactory,
    WeekdayFactory
)

from app.timetables.models import (
    Course, Dish, Event, Meal, MenuItem, Serving, ServingAutoUpdate, Timetable,
    Vendor, VendorService, Weekday
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
            cycle_length=self.timetable.cycle_length,
            ref_cycle_day=self.timetable.ref_cycle_day,
            ref_cycle_date=self.timetable.ref_cycle_date,
            description=self.timetable.description
        )

    def test_duplicate_timetable_name_cannot_be_saved(self):
        self.another_timetable.name = 'fellows timetable'

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
        test_date = datetime.date(2016, 11, 23)
        self.assertEqual(13, self.timetable.calculate_cycle_day(test_date))

        test_date = datetime.date(2016, 11, 24)
        self.assertEqual(14, self.timetable.calculate_cycle_day(test_date))

        test_date = datetime.date(2016, 11, 25)
        self.assertEqual(1, self.timetable.calculate_cycle_day(test_date))

        # test_date equal to ref_cycle_date
        test_date = self.timetable.ref_cycle_date
        cycle_day = self.timetable.ref_cycle_day
        self.assertEqual(cycle_day, self.timetable.calculate_cycle_day(test_date))

        # test_date earlier than ref_cycle_date cannot be resolved to a valid cycle_day
        test_date = datetime.date(2016, 9, 25)
        self.assertRaises(ValidationError, self.timetable.calculate_cycle_day, test_date)

    def test_get_vendors(self):
        vendor_service = VendorServiceFactory(timetable=self.timetable)

        new_vendors = [VendorFactory(name=x) for x in ['Spicy Foods', 'Tantalizer']]
        start_date = datetime.date(2016, 10, 1)
        end_date = datetime.date(2016, 11, 30)

        for new_vendor in new_vendors:
            VendorServiceFactory(
                timetable=self.timetable,
                vendor=new_vendor,
                start_date=start_date,
                end_date=end_date
            )

        test_date = datetime.date(2016, 11, 25)
        self.assertEqual(new_vendors, self.timetable.get_vendors(test_date))

        test_date = datetime.date(2008, 2, 23)
        self.assertEqual([vendor_service.vendor], self.timetable.get_vendors(test_date))

        test_date = datetime.date(2000, 2, 23)
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
        self.assertRaises(ValidationError, self.another_serving.save)


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


class ServingAutoUpdateTest(TestCase):
    """Test the ServingAutoUpdate model."""

    def setUp(self):
        self.vendor_service = VendorServiceFactory(start_date=None, end_date=None)
        self.timetable = self.vendor_service.timetable
        self.vendor = self.vendor_service.vendor
        self.date = self.timetable.ref_cycle_date
        self.earlier_date = datetime.date(2016, 9, 4)
        self.later_date = datetime.date(2016, 10, 4)

        meal = MealFactory()
        course = CourseFactory(name='main')
        dish_names = ['Quaker Oat and Moi-moi', 'Bread and Egg', 'Apples']
        self.menu_items = []
        for dish_name in dish_names:
            dish = DishFactory(name=dish_name)
            menu_item = MenuItemFactory(
                timetable=self.timetable,
                meal=meal,
                course=course,
                dish=dish
            )
            self.menu_items.append(menu_item)

    def get_servings_count(self):
        return Serving.objects.filter(
            menu_item__in=self.menu_items,
            vendor=self.vendor,
            date_served=self.date
        ).count()

    def test_get_menu_items_for_a_date_earlier_than_ref_cycle_date(self):
        self.assertRaises(
            ValidationError,
            ServingAutoUpdate.get_menu_items,
            self.timetable, self.earlier_date
        )

    def test_get_menu_items_with_no_menu_item_entry_for_combination_of_timetable_and_date(self):
        self.assertRaises(
            ValidationError,
            ServingAutoUpdate.get_menu_items,
            self.timetable, self.earlier_date
        )

    def test_get_menu_items_for_right_combination_of_timetable_and_date(self):
        menu_items = ServingAutoUpdate.get_menu_items(self.timetable, self.date)
        self.assertEqual(self.menu_items, list(menu_items))

    def test_verify_vendor_is_serving_for_dates_vendor_is_not_serving_specified_timetable(self):
        self.vendor_service.end_date = self.earlier_date
        self.vendor_service.save()

        self.assertRaises(
            ValidationError,
            ServingAutoUpdate.verify_vendor_is_serving,
            self.timetable, self.vendor, self.later_date
        )

    def test_verify_vendor_is_serving_for_dates_vendor_serves_specified_timetable(self):
        result = ServingAutoUpdate.verify_vendor_is_serving(
            self.timetable,
            self.vendor,
            self.earlier_date
        )
        self.assertEqual(None, result)

    def test_create_servings_if_not_exist_with_no_menu_item_entry_for_the_timetable_and_date(self):
        self.assertRaises(
            ValidationError,
            ServingAutoUpdate.create_servings_if_not_exist,
            self.timetable, self.vendor, self.earlier_date
        )

    def test_create_servings_if_not_exist_for_a_date_earlier_than_ref_cycle_date(self):
        self.assertRaises(
            ValidationError,
            ServingAutoUpdate.create_servings_if_not_exist,
            self.timetable, self.vendor, self.earlier_date
        )

    def test_create_servings_if_not_exist_for_dates_vendor_is_not_serving_specified_timetable(self):
        self.vendor_service.end_date = self.earlier_date
        self.vendor_service.save()

        self.assertRaises(
            ValidationError,
            ServingAutoUpdate.create_servings_if_not_exist,
            self.timetable, self.vendor, self.date
        )

    def test_create_servings_if_not_exist_for_right_combination_of_timetable_vendor_date(self):
        # Before create_servings_if_not_exist is called
        self.assertEqual(0, self.get_servings_count())

        # After create_servings_if_not_exist is called
        ServingAutoUpdate.create_servings_if_not_exist(self.timetable, self.vendor, self.date)
        self.assertEqual(3, self.get_servings_count())

    def test_get_servings_with_no_menu_item_entry_for_combination_of_timetable_and_date(self):
        self.assertRaises(
            ValidationError,
            ServingAutoUpdate.get_servings,
            self.timetable, self.later_date, vendor=self.vendor
        )

    def test_get_servings_for_a_date_earlier_than_ref_cycle_date(self):
        try:
            with transaction.atomic():
                ServingAutoUpdate.get_servings(
                    self.timetable,
                    self.earlier_date,
                    vendor=self.vendor
                )
        except ValidationError as e:
            self.assertEqual(
                ['Supply a date later than or equal to {}'.format(self.date)],
                e.messages
            )

    def test_get_servings_for_dates_vendor_is_not_serving_specified_timetable(self):
        self.vendor_service.end_date = self.earlier_date
        self.vendor_service.save()

        self.assertRaises(
            ValidationError,
            ServingAutoUpdate.get_servings,
            self.timetable, self.date, vendor=self.vendor
        )

    def test_get_servings_for_right_combination_of_timetable_and_vendor_and_date(self):
        # Before get_servings is called
        kwargs = {
            'timetable': self.timetable,
            'vendor': self.vendor,
            'date': self.date
        }
        self.assertRaises(
            ServingAutoUpdate.DoesNotExist,
            ServingAutoUpdate.objects.get,
            **kwargs
        )

        # After get_servings is called
        servings = ServingAutoUpdate.get_servings(self.timetable, self.date, vendor=self.vendor)
        self.assertIsInstance(ServingAutoUpdate.objects.get(**kwargs), ServingAutoUpdate)
        self.assertEqual(3, len(servings))
        self.assertIsInstance(servings[0], Serving)

    def test_get_servings_for_right_combination_of_timetable_and_date_without_vendor(self):
        # Before get_servings is called
        kwargs = {
            'timetable': self.timetable,
            'date': self.date
        }
        self.assertRaises(
            ServingAutoUpdate.DoesNotExist,
            ServingAutoUpdate.objects.get,
            **kwargs
        )

        # After get_servings is called
        servings = ServingAutoUpdate.get_servings(self.timetable, self.date)
        self.assertIsInstance(ServingAutoUpdate.objects.get(**kwargs), ServingAutoUpdate)
        self.assertEqual(3, len(servings))
        self.assertIsInstance(servings[0], Serving)

    def test_manual_creation_of_serving_auto_update(self):
        # Before creation attempt
        kwargs = {
            'timetable': self.timetable,
            'vendor': self.vendor,
            'date': self.date
        }
        self.assertRaises(
            ServingAutoUpdate.DoesNotExist,
            ServingAutoUpdate.objects.get,
            **kwargs
        )
        self.assertEqual(0, self.get_servings_count())

        # After creation attempt with timetable and date combination with no menu_item entry
        serving_auto_update = ServingAutoUpdate(
            timetable=self.timetable,
            vendor=self.vendor,
            date=self.later_date
        )
        self.assertRaises(ValidationError, serving_auto_update.save)

        # After creation attempt with right combination of timetable, vendor and date
        serving_auto_update.date = self.date
        serving_auto_update.save()
        self.assertIsInstance(ServingAutoUpdate.objects.get(**kwargs), ServingAutoUpdate)
        self.assertEqual(3, self.get_servings_count())
