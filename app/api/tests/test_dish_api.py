from base64 import b64encode

from django.contrib.auth.models import User
from django.test import Client, TestCase


class DishApiTest(TestCase):
    """Test for Dish API"""

    def setUp(self):
        self.client = Client()
        self.endpoint = '/api'
        self.data = {
            'name': 'rice',
            'description': 'white rice'
        }
        self.dishes = (
            ('rice', 'white rice'),
            ('Coconut rice', 'rice with coconut flavor'),
            ('plantain', 'fried plantain'),
        )
        self.admin_test_credentials = ('admin', 'admin@taverna.com', 'qwerty123')
        self.create_admin_account()
        self.header = {'HTTP_X_TAVERNATOKEN': self.obtain_api_key()}

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

    def make_request(self, query):
        return self.client.post(self.endpoint, {'query': query}, **self.header).json()

    def create_dish(self, name, description):
        query = '''
            mutation{
              createDish(input: {name: "%s", description: "%s"}){
                dish{
                  id,
                  originalId,
                  name
                }
              }
            }
        ''' % (name, description)

        return self.make_request(query)

    def create_multiple_dishes(self):
        return [self.create_dish(name, description) for name, description in self.dishes]

    def retrieve_dish(self, id):
        query = 'query {dish(id: "%s" ) {name}}' % (id)

        return self.make_request(query)

    def test_creation_of_dish_object(self):
        response = self.create_dish(self.data['name'], self.data['description'])
        expected = {
            'createDish': {
                'dish': {
                    'id': response['data']['createDish']['dish']['id'],
                    'originalId': response['data']['createDish']['dish']['originalId'],
                    'name': self.data['name']
                }
            }
        }

        self.assertEqual(expected, response['data'])

    def test_retrieval_of_one_dish_object(self):
        expected = {
            'dish': {
                'name': self.data['name']
            }
        }
        create_response = self.create_dish(self.data['name'], self.data['description'])
        response = self.retrieve_dish(create_response['data']['createDish']['dish']['id'])

        self.assertEqual(expected, response['data'])

    def test_retrieval_of_multiple_dish_objects_without_filtering(self):
        self.create_multiple_dishes()

        query = 'query {dishes{edges{node{name}}}}'

        expected = {
            'dishes': {
                'edges': [
                  {
                    'node': {
                        'name': self.dishes[0][0]
                    }
                  },
                  {
                    'node': {
                        'name': self.dishes[1][0]
                    }
                  },
                  {
                    'node': {
                        'name': self.dishes[2][0]
                    }
                  }
                ]
            }
        }

        response = self.make_request(query)

        self.assertEqual(expected, response['data'])

    def test_retrieval_of_multiple_user_objects_filter_by_username(self):
        self.create_multiple_dishes()
        query = 'query {dishes(name_Icontains: "Rice") {edges{node{name}}}}'

        expected = {
            'dishes': {
                'edges': [
                  {
                    'node': {
                        'name': self.dishes[0][0]
                    }
                  },
                  {
                    'node': {
                        'name': self.dishes[1][0]
                    }
                  }
                ]
            }
        }

        response = self.make_request(query)

        self.assertEqual(expected, response['data'])

    def test_update_of_dish_object(self):
        create_response = self.create_dish(self.data['name'], self.data['description'])
        query = '''
            mutation{
                updateDish(
                    input: {
                        id: "%s",
                        name: "rice edited"
                    }
                )
                {
                    dish{
                        id,
                        name
                    }
                }
            }
        ''' % (create_response['data']['createDish']['dish']['id'])

        expected = {
            "updateDish": {
                "dish": {
                    "id": create_response['data']['createDish']['dish']['id'],
                    "name": "rice edited"
                }
            }
        }

        response = self.make_request(query)

        self.assertEqual(expected, response['data'])

    def test_deletion_of_dish_object(self):
        create_response = self.create_dish(self.data['name'], self.data['description'])
        query = '''
            mutation{
                deleteDish(input: {id: "%s"}){
                    dish{
                        name
                    }
                }
            }
        ''' % (create_response['data']['createDish']['dish']['id'])

        expected = {
            "deleteDish": {
                "dish": {
                    "name": self.data['name']
                }
            }
        }

        response = self.make_request(query)
        self.assertEqual(expected, response['data'])

        response = self.retrieve_dish(create_response['data']['createDish']['dish']['id'])
        self.assertEqual(None, response['data']['dish'])

    def ordering_test_helper(self, ordering_param, records):
        # For ascending ordering
        query = 'query{dishes(orderBy: "%s") {edges{node{name}}}}' % (ordering_param)
        expected = {
            'dishes': {
                'edges': [
                  {
                    'node': {
                        'name': records[0]
                    }
                  },
                  {
                    'node': {
                        'name': records[1]
                    }
                  },
                  {
                    'node': {
                        'name': records[2]
                    }
                  }
                ]
            }
        }
        response = self.make_request(query)
        self.assertEqual(expected, response['data'])

        # For descending ordering
        query = 'query {dishes(orderBy: "-%s") {edges{node{name}}}}' % (ordering_param)
        expected['dishes']['edges'].reverse()
        response = self.make_request(query)
        self.assertEqual(expected, response['data'])

    def test_retrieval_of_multiple_dish_objects_ordering_by_id(self):
        self.create_multiple_dishes()
        records = [
            self.dishes[0][0],
            self.dishes[1][0],
            self.dishes[2][0]
        ]

        self.ordering_test_helper('id', records)

    def test_retrieval_of_multiple_dish_objects_ordering_by_name(self):
        self.create_multiple_dishes()
        records = [
            self.dishes[1][0],
            self.dishes[2][0],
            self.dishes[0][0]
        ]

        self.ordering_test_helper('name', records)
