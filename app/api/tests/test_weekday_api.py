from django.test import Client, TestCase

from .utils import obtain_api_key, create_admin_account


class WeekdayApiTest(TestCase):
    """Tests for Weekday API."""

    def setUp(self):
        self.client = Client()
        self.endpoint = '/api'
        self.admin_test_credentials = ('admin', 'admin@taverna.com', 'qwerty123')
        create_admin_account(*self.admin_test_credentials)
        self.header = {
            'HTTP_X_TAVERNATOKEN': obtain_api_key(
                self.client, *self.admin_test_credentials
            )
        }
        self.weekdays = ('weekday1', 'weekday2',)
        self.first_weekday = self.create_weekday('day1')['weekday']

    def make_request(self, query, method='GET'):
        if method == 'GET':
            return self.client.get(self.endpoint, data={'query': query}, **self.header).json()

        if method == 'POST':
            return self.client.post(self.endpoint, data={'query': query}, **self.header).json()

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

        return self.make_request(query, 'POST')

    def retrieve_weekday(self, weekday_id):
        query = 'query {weekday(id: "%s") {name}}' % (weekday_id)

        return self.make_request(query)

    def create_multiple_weekdays(self):
        return [self.create_weekday(name) for name in self.weekdays]

    def test_creation_of_weekday_object(self):
        # For new weekday record
        response = self.create_weekday('day2')
        created_weekday = response['weekday']
        expected = {
            'weekday': {
                'id': created_weekday['id'],
                'originalId': created_weekday['originalId'],
                'name': 'day2'
            }
        }
        self.assertEqual(expected, response)

        # For existing weekday record
        self.assertEqual({'weekday': None}, self.create_weekday('day1'))

    def test_retrieve_weekday_object(self):
        # Retrieve with valid id
        response = self.retrieve_weekday(self.first_weekday['id'])
        expected = {
            'weekday': {
                'name': self.first_weekday['name']
            }
        }
        self.assertEqual(expected, response)

        # Retrieve with invalid id
        self.assertEqual({'weekday': None}, self.retrieve_weekday(100))

    def test_retrieve_multiple_weekdays_without_filtering(self):
        self.create_multiple_weekdays()

        query = 'query {weekdays{edges{node{name}}}}'

        expected = {
            'weekdays': [
                {
                    'name': self.first_weekday['name']
                },
                {
                    'name': self.weekdays[0]
                },
                {
                    'name': self.weekdays[1]
                }
            ]
        }

        response = self.make_request(query)

        self.assertEqual(expected, response)

    def test_retrieve_multiple_users_filter_by_name(self):
        self.create_multiple_weekdays()
        query = 'query {weekdays(name_Icontains: "day1") {edges{node{name}}}}'

        expected = {
            'weekdays': [
                {
                    'name': self.first_weekday['name']
                },
                {
                    'name': self.weekdays[0]
                }
            ]
        }

        response = self.make_request(query)

        self.assertEqual(expected, response)

    def test_update_weekday_object(self):
        # Update with valid id
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
        response = self.make_request(query, 'POST')
        expected = {
            'weekday': {
                'id': self.first_weekday['id'],
                'originalId': self.first_weekday['originalId'],
                'name': 'day3'
            }
        }
        self.assertEqual(expected, response)

        # Update with invalid id
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
        ''' % (100)
        self.assertEqual({'weekday': None}, self.make_request(query, 'POST'))

    def test_deletion_weekday_object(self):
        # Delete with valid id
        query = '''
            mutation{
                deleteWeekday(input: {id: "%s"}){
                    weekday{
                        name
                    }
                }
            }
        ''' % (self.first_weekday['id'])
        response = self.make_request(query, 'POST')
        expected = {
            'weekday': {
                'name': self.first_weekday['name']
            }
        }
        self.assertEqual(expected, response)
        self.assertEqual({'weekday': None}, self.retrieve_weekday(self.first_weekday['id']))

        # Delete with invalid id
        query = '''
            mutation{
                deleteWeekday(input: {id: "%s"}){
                    weekday{
                        name
                    }
                }
            }
        ''' % (100)
        self.assertEqual({'weekday': None}, self.make_request(query, 'POST'))
