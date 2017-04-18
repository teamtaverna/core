from django.test import Client, TestCase

from .utils import obtain_api_key, create_admin_account


class DishApiTest(TestCase):
    """Test for Dish API"""

    def setUp(self):
        self.client = Client()
        self.endpoint = '/api'
        self.admin_test_credentials = ('admin', 'admin@taverna.com', 'qwerty123')
        create_admin_account(*self.admin_test_credentials)
        self.data = {
            'name': 'rice',
            'description': 'white rice'
        }
        self.dishes = (
            ('rice', 'white rice'),
            ('Coconut rice', 'rice with coconut flavor'),
            ('plantain', 'fried plantain'),
        )
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

        return self.make_request(query, 'POST')

    def create_multiple_dishes(self):
        return [self.create_dish(name, description) for name, description in self.dishes]

    def retrieve_dish(self, id):
        query = 'query {dish(id: "%s" ) {name}}' % (id)

        return self.make_request(query)

    def ordering_test_helper(self, ordering_param, records):
        # For ascending ordering
        query = 'query{dishes(orderBy: "%s") {edges{node{name}}}}' % (ordering_param)
        expected = {
            'dishes': [
                {
                    'name': records[0]
                },
                {
                    'name': records[1]
                },
                {
                    'name': records[2]
                }
            ]
        }
        response = self.make_request(query)
        self.assertEqual(expected, response)

        # For descending ordering
        query = 'query {dishes(orderBy: "-%s") {edges{node{name}}}}' % (ordering_param)
        expected['dishes'].reverse()
        response = self.make_request(query)
        self.assertEqual(expected, response)

    def test_creation_of_dish_object(self):
        # For new dish record
        response = self.create_dish(self.data['name'], self.data['description'])
        created_dish = response['dish']
        expected = {
            'dish': {
                'id': created_dish['id'],
                'originalId': created_dish['originalId'],
                'name': self.data['name']
            }
        }
        self.assertEqual(expected, response)

        # For existing weekday record
        response = self.create_dish(self.data['name'], self.data['description'])
        self.assertEqual({'dish': None}, response)

    def test_retrieval_of_one_dish_object(self):
        # Retrieve with valid id
        expected = {
            'name': self.data['name']
        }
        create_response = self.create_dish(self.data['name'], self.data['description'])
        response = self.retrieve_dish(create_response['dish']['id'])
        self.assertEqual(expected, response['dish'])

        # Retrieve with invalid id
        self.assertEqual({'dish': None}, self.retrieve_dish(2))

    def test_retrieval_of_multiple_dish_objects_without_filtering(self):
        self.create_multiple_dishes()

        query = 'query {dishes{edges{node{name}}}}'

        expected = {
            'dishes': [
                {
                    'name': self.dishes[0][0]
                },
                {
                    'name': self.dishes[1][0]
                },
                {
                    'name': self.dishes[2][0]
                }
            ]
        }

        response = self.make_request(query)

        self.assertEqual(expected, response)

    def test_retrieval_of_multiple_user_objects_filter_by_username(self):
        self.create_multiple_dishes()
        query = 'query {dishes(name_Icontains: "Rice") {edges{node{name}}}}'

        expected = {
            'dishes': [
                {
                    'name': self.dishes[0][0]
                },
                {
                    'name': self.dishes[1][0]
                }
            ]
        }

        response = self.make_request(query)

        self.assertEqual(expected, response)

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

    def test_update_of_dish_object(self):
        # Update with valid id
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
        ''' % (create_response['dish']['id'])
        expected = {
            'dish': {
                'id': create_response['dish']['id'],
                'name': 'rice edited'
            }
        }
        response = self.make_request(query, 'POST')
        self.assertEqual(expected, response)

        # Update with invalid id
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
        ''' % ('wrong-id')
        self.assertEqual({'dish': None}, self.make_request(query, 'POST'))

    def test_deletion_of_dish_object(self):
        # Delete with valid id
        create_response = self.create_dish(self.data['name'], self.data['description'])
        query = '''
            mutation{
                deleteDish(input: {id: "%s"}){
                    dish{
                        name
                    }
                }
            }
        ''' % (create_response['dish']['id'])
        expected = {
            'dish': {
                'name': self.data['name']
            }
        }
        response = self.make_request(query, 'POST')
        self.assertEqual(expected, response)
        self.assertEqual({'dish': None}, self.retrieve_dish(create_response['dish']['id']))

        # Delete with invalid id
        query = '''
            mutation{
                deleteDish(input: {id: "%s"}){
                    dish{
                        name
                    }
                }
            }
        ''' % ('wrong-id')
        self.assertEqual({'dish': None}, self.make_request(query, 'POST'))
