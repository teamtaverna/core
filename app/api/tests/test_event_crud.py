from django.test import Client, TestCase

from .utils import create_admin_account, make_request
from app.timetables.factories import EventFactory


class EventApiTest(TestCase):

    def setUp(self):
        self.client = Client()
        create_admin_account()
        self.event = EventFactory()

    def retrieve_event(self):
        query = 'query {event{name}}'
        return make_request(self.client, query)

    def test_retrieve_events(self):
        response = self.retrieve_event()
        expected = {'events': [{
            'name': self.event.name
        }]}
        self.assertEqual(expected, response)
