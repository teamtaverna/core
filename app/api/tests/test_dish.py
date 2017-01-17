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

        return self.client.post(self.endpoint, {'query': query}).json()

    def retrieve_dish(self, id):
        query = 'query {dish(id: "%s" ) {username}}' % (id)

        return self.client.post(self.endpoint, data={'query': query}).json()

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
