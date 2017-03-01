from base64 import b64encode

from django.test import Client, TestCase
from django.contrib.auth.models import User


class WeekdayApiTest(TestCase):
    """Tests for Weekday API."""

    def setUp(self):
        self.client = Client()
        self.endpoint = '/api'
        self.admin_test_credentials = ('admin', 'admin@taverna.com',
                                       'qwerty123')
        self.create_admin_account()
        self.header = {'HTTP_X_TAVERNATOKEN': self.obtain_api_key()}

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

    def obtain_api_key(self):
        credentials = '{}:{}'.format(
            self.admin_test_credentials[0],
            self.admin_test_credentials[2]
        )
        b64_encoded_credentials = b64encode(credentials.encode('utf-8'))

        return self.client.post(
            '/api/api_key',
            **{'HTTP_AUTHORIZATION': 'Basic %s' % b64_encoded_credentials.decode('utf-8')}
        ).json()['api_key']

    def create_admin_account(self):
        User.objects.create_superuser(*self.admin_test_credentials)

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
        self.create_weekday('day1')
        response = self.create_weekday('day1')
        expected = {
            'createWeekday': {
                'weekday': None
            }
        }

        self.assertEqual(expected, response['data'])
