from base64 import b64encode
import datetime

from django.contrib.auth.models import User
from django.test import Client, TestCase


class MealApiTest(TestCase):
    """Test for Meal API"""
    def setUp(self):
        self.client = Client()
        self.maxDiff = None  # debugging
        self.endpoint = '/api'
        self.admin_test_credentials = ('admin', 'admin@taverna.com', 'qwerty123')
        self.create_admin_account()
        self.header = {'HTTP_X_TAVERNATOKEN': self.obtain_api_key()}

        self.data = {
            'name': 'BreakFast',
            'start_time': datetime.time(8, 30, 0),
            'end_time': datetime.time(10, 0, 0)
        }

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

    def make_request(self, query, method='GET'):
        if method == 'GET':
            return self.client.post(self.endpoint, {'query': query}, **self.header).json()

        if method == 'POST':
            return self.client.post(self.endpoint, data={'query': query}, **self.header).json()

    def retrieve_meal(self, id):
        query = 'query {meal(id: "%s" ) {name}' % (id)

        return self.make_request(query)

    def create_meal(self, name, start_time, end_time):
        query = '''
            mutation {
                createMeal(input: {name: "%s", startTime: "%s",  endTime: "%s"}){
                    meal{
                        id,
                        originalId,
                        name
                    }
                }
            }
        ''' % (name, start_time, end_time)

        return self.make_request(query)

    def review_meal(self, meal_id, review_msg, review_stars):
        query = '''

        '''

    def test_creation_of_meal_object(self):
        response = self.create_meal(self.data['name'], self.data['start_time'], self.data['end_time'])
        expected = {
            'id': response['id'],
            'originalId': response['originalId'],
            'name': self.data['name']
        }

        self.assertEqual(expected, response)

    def test_updating_of_meal_object(self):
        create_response = self.create_meal(self.data['name'], self.data['start_time'], self.data['end_time'])
        # Update with valid id
        query = '''
            mutation{
                updateMeal(
                    input: {
                        id: "%s",
                        name: "breakfast edited"
                    }
                )
                {
                    meal{
                        id,
                        name
                    }
                }
            }
        ''' % (create_response['id'])
        expected = {
            'id': create_response['id'],
            'name': 'breakfast edited'
        }
        response = self.make_request(query, 'POST')
        self.assertEqual(expected, response)

        # Update with invalid id
        query = '''
            mutation{
                updateMeal(
                    input: {
                        id: "%s",
                        name: "breakfast edited"
                    }
                )
                {
                    meal{
                        id,
                        name
                    }
                }
            }
        ''' % ("wrong-id")
        self.assertEqual(None, self.make_request(query, 'POST'))

    def test_deletion_of_meal_object(self):
        pass

    def test_review_of_meal_object(self):
        pass


