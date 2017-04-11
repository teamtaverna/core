from base64 import b64encode
import datetime

from django.test import Client, TestCase
from django.contrib.auth.models import User

from app.api.tests.utils import obtain_api_key, create_admin_account


class MealApiTest(TestCase):
    """Test for Meal API"""

    def setUp(self):
        self.client = Client()
        self.endpoint = '/api'
        self.admin_test_credentials = ('admin', 'admin@taverna.com', 'qwerty123')
        create_admin_account(*self.admin_test_credentials)
        self.data = {
            'name': 'BreakFast',
            'start_time': datetime.time(8, 30, 0),
            'end_time': datetime.time(10, 0, 0)
        }
        self.header = {
            'HTTP_X_TAVERNATOKEN': obtain_api_key(
                self.client, *self.admin_test_credentials
            )
        }

    def make_request(self, query, method='GET'):
        if method == 'GET':
            return self.client.get(self.endpoint, data={'query': query}, **self.header).json()

        if method == 'POST':
            return self.client.post(self.endpoint, data={'query': query}, **self.header).json()

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

        return self.make_request(query, 'POST')

    def retrieve_meal(self, id):
        query = 'query {meal(id: "%s" ) {name}}' % (id)

        return self.make_request(query)

    def test_creation_of_meal_object(self):
        response = self.create_meal(self.data['name'], self.data['start_time'], self.data['end_time'])
        expected = {
            'id': response['id'],
            'originalId': response['originalId'],
            'name': self.data['name']
        }

        self.assertEqual(expected, response)


    def test_retrieval_of_one_meal_object(self):
        # Retrieve with valid id
        expected = {
            'name': self.data['name']
        }
        create_response = self.create_meal(self.data['name'], self.data['start_time'], self.data['end_time'])
        response = self.retrieve_meal(create_response['id'])
        self.assertEqual(expected, response)

        # Retrieve with invalid id
        self.assertEqual(None, self.retrieve_meal(2))

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
        # Delete with valid id
        create_response = self.create_meal(self.data['name'], self.data['start_time'], self.data['end_time'])
        query = '''
            mutation{
                deleteMeal(input: {id: "%s"}){
                    meal{
                        name
                    }
                }
            }
        ''' % (create_response['id'])
        expected = {
            "name": self.data['name']
        }
        response = self.make_request(query, 'POST')
        self.assertEqual(expected, response)
        self.assertEqual(None, self.retrieve_meal(create_response['id']))

        # Delete with invalid id
        query = '''
            mutation{
                deleteMeal(input: {id: "%s"}){
                    meal{
                        name
                    }
                }
            }
        ''' % ("wrong-id")
        self.assertEqual(None, self.make_request(query, 'POST'))
