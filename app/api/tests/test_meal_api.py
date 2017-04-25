import datetime

from django.test import Client, TestCase

from .utils import create_admin_account, make_request


class MealApiTest(TestCase):
    """Test for Meal API"""

    def setUp(self):
        self.client = Client()
        create_admin_account()
        self.data = {
            'name': 'BreakFast',
            'start_time': datetime.time(8, 30, 0),
            'end_time': datetime.time(10, 0, 0)
        }

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

        return make_request(self.client, query, method='POST')

    def retrieve_meal(self, id):
        query = 'query {meal(id: "%s" ) {name}}' % (id)

        return make_request(self.client, query)

    def test_creation_of_meal_object(self):
        response = self.create_meal(self.data['name'],
                                    self.data['start_time'],
                                    self.data['end_time'])
        created_meal = response['meal']
        expected = {
            'meal': {
                'id': created_meal['id'],
                'originalId': created_meal['originalId'],
                'name': self.data['name']
            }
        }

        self.assertEqual(expected, response)

    def test_retrieval_of_one_meal_object(self):
        # Retrieve with valid id
        expected = {
            'meal': {
                'name': self.data['name']
            }
        }
        create_response = self.create_meal(self.data['name'],
                                           self.data['start_time'],
                                           self.data['end_time'])
        response = self.retrieve_meal(create_response['meal']['id'])
        self.assertEqual(expected, response)

        # Retrieve with invalid id
        self.assertEqual({'meal': None}, self.retrieve_meal(2))

    def test_updating_of_meal_object(self):
        create_response = self.create_meal(self.data['name'],
                                           self.data['start_time'],
                                           self.data['end_time'])
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
        ''' % (create_response['meal']['id'])
        expected = {
            'meal': {
                'id': create_response['meal']['id'],
                'name': 'breakfast edited'
            }
        }
        response = make_request(self.client, query, 'POST')
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
        self.assertEqual({'meal': None}, make_request(self.client, query, 'POST'))

    def test_deletion_of_meal_object(self):
        # Delete with valid id
        create_response = self.create_meal(self.data['name'],
                                           self.data['start_time'],
                                           self.data['end_time'])
        query = '''
            mutation{
                deleteMeal(input: {id: "%s"}){
                    meal{
                        name
                    }
                }
            }
        ''' % (create_response['meal']['id'])
        expected = {
            'meal': {
                "name": self.data['name']
            }
        }
        response = make_request(self.client, query, 'POST')
        self.assertEqual(expected, response)
        self.assertEqual({'meal': None}, self.retrieve_meal(create_response['meal']['id']))

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
        self.assertEqual({'meal': None}, make_request(self.client, query, 'POST'))
