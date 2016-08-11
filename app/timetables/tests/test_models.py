from django.test import TestCase
from django.db import IntegrityError

from app.timetables.models import Weekday


class WeekdayTest(TestCase):
    """Tests the Weekday model."""

    def setUp(self):
        Weekday.objects.create(name="monday")

    def test_weekday_name_should_be_capitalized_on_save(self):
        day = Weekday.objects.get(name__iexact="monday")

        self.assertEqual(day.name, "Monday")

    def test_duplicate_weekday_name_cannot_be_saved(self):
        day = Weekday(name="Monday")

        self.assertRaises(IntegrityError, day.save)
