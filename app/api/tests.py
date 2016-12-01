from django.test import Client, TestCase


class ApiTest(TestCase):
    """Test for API"""
    fixtures = ['test_users']

    def setUp(self):
        self.client = Client()
        self.endpoint = '/api'

    def test_api_endpoint_is_live(self):
        response = self.client.get(self.endpoint, {'query': ''})

        self.assertEqual(400, response.status_code)
        self.assertEqual(
            'Must provide query string.',
            response.json()['errors'][0]['message']
        )

    def test_user_query(self):
        query = 'query {user(id: "VXNlck5vZGU6MQ==" ) {username}}'

        expected = {
            'user': {
                'username': 'demo'
            }
        }
        response = self.client.get(self.endpoint, {'query': query})
        self.assertEqual(200, response.status_code)
        self.assertRaises(KeyError, lambda: response.json()["errors"])
        self.assertEqual(expected, response.json()['data'])

    def test_users_query(self):
        query = 'query {users{edges{node{username}}}}'

        expected = {
            'users': {
                'edges': [
                  {
                    'node': {
                        'username': 'demo'
                    }
                  },
                  {
                    'node': {
                        'username': 'editor'
                    }
                  },
                  {
                    'node': {
                        'username': 'admin'
                    }
                  }
                ]
               }
            }
        response = self.client.get(self.endpoint, {'query': query})
        self.assertEqual(200, response.status_code)
        self.assertRaises(KeyError, lambda: response.json()["errors"])
        self.assertEqual(expected, response.json()['data'])

    def test_create_user_query(self):
        query = '''
            mutation{
              createUser(input: {username: "oakeem", password: "oatman"}){
                user{
                  username
                }
              }
            }
        '''
        expected = {
            "createUser": {
                "user": {
                    "username": "oakeem"
                }
            }
        }
        response = self.client.post(self.endpoint, {'query': query})
        self.assertEqual(200, response.status_code)
        self.assertRaises(KeyError, lambda: response.json()["errors"])
        self.assertEqual(expected, response.json()['data'])

    def test_update_user_query(self):
        query = '''
            mutation{
                updateUser(input: {id: "VXNlck5vZGU6MQ==", firstName: "Akeem",
                                   lastName: "Oduola", email: "akeem.oduola@andela.com",
                                   username: "oakeem"}){
                    user{
                        originalId
                        username
                        firstName
                        lastName
                        email
                    }
                }
            }
        '''
        expected = {
            "updateUser": {
                "user": {
                    "originalId": 1,
                    "username": "oakeem",
                    "firstName": "Akeem",
                    "lastName": "Oduola",
                    "email": "akeem.oduola@andela.com",
                }
            }
        }
        response = self.client.post(self.endpoint, {'query': query})
        self.assertEqual(200, response.status_code)
        self.assertRaises(KeyError, lambda: response.json()["errors"])
        self.assertEqual(expected, response.json()['data'])

    def test_delete_user_query(self):
        query = '''
            mutation{
                deleteUser(input: {id: "VXNlck5vZGU6MQ=="}){
                    user{
                        username
                    }
                }
            }
        '''
        expected = {
            "deleteUser": {
                "user": {
                    "username": "demo"
                }
            }
        }
        response = self.client.post(self.endpoint, {'query': query})
        self.assertEqual(200, response.status_code)
        self.assertRaises(KeyError, lambda: response.json()["errors"])
        self.assertEqual(expected, response.json()['data'])
