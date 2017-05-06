from django.test import Client, TestCase

from .utils import create_admin_account, make_request
from app.timetables.factories import TimetableFactory


class TimetableApiTest(TestCase):

    def setUp(self):
        self.client = Client()
        create_admin_account()
        self.timetable = TimetableFactory()

    def retrieve_timetables(self):
        query = 'query {timetables{edges{node{name}}}}'

        return make_request(self.client, query)

    def test_retrieve_timetables(self):
        response = self.retrieve_timetables()
        expected = {
            'timetables': [{
                'name': self.timetable.name
            }]
        }
        self.assertEqual(expected, response)
