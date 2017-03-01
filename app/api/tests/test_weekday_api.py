from django.test import Client, TestCase

from .utils import obtain_api_key, create_admin_account


class WeekdayApiTest(TestCase):
    """Tests for Weekday API."""

    def setUp(self):
        self.client = Client()
        self.endpoint = '/api'
        self.admin_test_credentials = ('admin', 'admin@taverna.com',
                                       'qwerty123')
        self.create_admin_account = create_admin_account(
            *self.admin_test_credentials
        )
        self.header = {
            'HTTP_X_TAVERNATOKEN': obtain_api_key(
                self.client, *self.admin_test_credentials
            )
        }

        response = self.create_weekday('day1')
        self.first_weekday = response['data']['createWeekday']['weekday']

    def create_weekday(self, name):
        query = '''
                mutation{
                    createWeekday(input: {name: "%s"}){
                        weekday{
                            id,
                            originalId,
                            name
                        }
                    }
                }
                ''' % (name)

        return self.client.post(
            self.endpoint, {'query': query}, **self.header
        ).json()

    def retrieve_weekday(self, weekday_id):
        query = 'query {weekday(id: "%s") {name}}' % (weekday_id)

        return self.client.get(
            self.endpoint, data={'query': query}, **self.header
        ).json()

    def test_creation_of_weekday_object(self):
        response = self.create_weekday('day2')
        expected = {
            'createWeekday': {
                'weekday': {
                    'id': response['data']['createWeekday']['weekday']['id'],
                    'originalId': response['data']['createWeekday']['weekday']['originalId'],
                    'name': 'day2'
                }
            }
        }

        self.assertEqual(expected, response['data'])

    def test_weekday_object_duplicate(self):
        response = self.create_weekday('day1')
        expected = {
            'createWeekday': {
                'weekday': None
            }
        }

        self.assertEqual(expected, response['data'])

    def test_retrieve_weekday_object(self):
        response = self.retrieve_weekday(self.first_weekday['id'])
        expected = {
            'weekday': {
                'name': self.first_weekday['name']
            }
        }

        self.assertEqual(expected, response['data'])

    def test_update_weekday_object(self):
        query = '''
                mutation{
                    updateWeekday(
                        input: {
                            id: "%s",
                            name: "day3"
                        }
                    )
                    {
                        weekday{
                            id,
                            originalId,
                            name
                        }
                    }
                }
                ''' % (self.first_weekday['id'])

        response = self.client.post(
            self.endpoint,
            data={
                'query': query
            },
            **self.header
        ).json()

        expected = {
            'updateWeekday': {
                'weekday': {
                    'id': self.first_weekday['id'],
                    'originalId': self.first_weekday['originalId'],
                    'name': 'day3'
                }
            }
        }

        self.assertEqual(expected, response['data'])

    def test_deletion_weekday_object(self):
        query = '''
            mutation{
                deleteWeekday(input: {id: "%s"}){
                    weekday{
                        name
                    }
                }
            }
        ''' % (self.first_weekday['id'])

        response = self.client.post(
            self.endpoint,
            data={
                'query': query
            },
            **self.header
        ).json()

        expected = {
            "deleteWeekday": {
                "weekday": {
                    "name": self.first_weekday['name']
                }
            }
        }

        self.assertEqual(expected, response['data'])

        # Verify that the object does not exist anymore
        response = self.retrieve_weekday(self.first_weekday['id'])
        self.assertEqual(
            None, response['data']['weekday']
        )
