from django.test import Client, TestCase

from app.timetables.factories import (
    CourseFactory, DishFactory, MealFactory, MenuItemFactory,
    VendorServiceFactory,
)
from .utils import create_admin_account, make_request


class ServingApiTest(TestCase):
    """Tests for Serving API."""

    def setUp(self):
        self.vendor_service = VendorServiceFactory(start_date=None, end_date=None)
        self.timetable = self.vendor_service.timetable
        self.vendor = self.vendor_service.vendor
        self.date = self.timetable.ref_cycle_date

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

        self.client = Client()
        create_admin_account()

    def retrieve_servings(self, timetable, date, vendor=None):
        if vendor:
            query_args = 'timetable: "{}", vendor: "{}", date: "{}"'.format(
                timetable, vendor, date
            )
        else:
            query_args = 'timetable: "{}", date: "{}"'.format(timetable, date)

        query = '''query {servings(%s) {
                    dateServed
                    vendor {
                        name
                    }
                    menuItem {
                        cycleDay
                        meal {
                            name
                        }
                        course {
                            name
                            sequenceOrder
                        }
                        dish {
                            name
                        }
                        timetable {
                            name
                        }
                    }
                }}''' % (query_args)

        return make_request(self.client, query)

    def test_retrieval_of_servings(self):
        # Retrieve with valid combo
        response = self.retrieve_servings(
            self.timetable.slug,
            self.date.isoformat(),
            vendor=self.vendor.slug
        )
        expected = {
            'servings': [
                {
                    'dateServed': self.date.isoformat(),
                    'vendor': {
                        'name': self.vendor.name,
                    },
                    'menuItem': {
                        'cycleDay': menu_item.cycle_day,
                        'meal': {
                            'name': menu_item.meal.name,
                        },
                        'course': {
                            'name': menu_item.course.name,
                            'sequenceOrder': menu_item.course.sequence_order,
                        },
                        'dish': {
                            'name': menu_item.dish.name,
                        },
                        'timetable': {
                            'name': self.timetable.name,
                        }
                    }
                } for menu_item in self.menu_items
            ]
        }

        for x in response['servings']:
            self.assertIn(x, expected['servings'])

        # Retrieve with invalid combo
        self.assertIn(
            'error',
            self.retrieve_servings(self.timetable.slug+'d', self.vendor.slug, self.date.isoformat())
        )

    def test_retrieval_of_servings_without_specifying_vendor(self):
        # Retrieve with valid combo
        response = self.retrieve_servings(
            self.timetable.slug,
            self.date.isoformat()
        )
        expected = {
            'servings': [
                {
                    'dateServed': self.date.isoformat(),
                    'vendor': {
                        'name': self.vendor.name,
                    },
                    'menuItem': {
                        'cycleDay': menu_item.cycle_day,
                        'meal': {
                            'name': menu_item.meal.name,
                        },
                        'course': {
                            'name': menu_item.course.name,
                            'sequenceOrder': menu_item.course.sequence_order,
                        },
                        'dish': {
                            'name': menu_item.dish.name,
                        },
                        'timetable': {
                            'name': self.timetable.name,
                        }
                    }
                } for menu_item in self.menu_items
            ]
        }

        for x in response['servings']:
            self.assertIn(x, expected['servings'])
