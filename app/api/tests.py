from django.test import Client, TestCase


class UserApiTest(TestCase):
    """Test for User API"""

    def setUp(self):
        self.client = Client()
        self.endpoint = '/api'

        response = self.create_user('oakeem', 'oatman')
        self.first_user = response['data']['createUser']['user']

    def create_user(self, username, password):
        query = '''
            mutation{
              createUser(input: {username: "%s", password: "%s"}){
                user{
                  id,
                  originalId,
                  username
                }
              }
            }
        ''' % (username, password)

        return self.client.post(self.endpoint, {'query': query}).json()

    def create_multiple_users(self):
        new_users = (
            ('john', 'qwerty123'),
            ('raphael', 'qwerty123'),
            ('samson', 'qwerty123'),
        )

        [self.create_user(username, password) for username, password in new_users]

        return new_users

    def retrieve_user(self, user_id):
        query = 'query {user(id: "%s" ) {username}}' % (user_id)

        return self.client.post(self.endpoint, data={'query': query}).json()

    def ordering_test_helper(self, ordering_param, users):
        # For ascending ordering
        query = 'query{users(orderBy: "%s") {edges{node{username}}}}' % (ordering_param)
        expected = {
            'users': {
                'edges': [
                  {
                    'node': {
                        'username': users[0]
                    }
                  },
                  {
                    'node': {
                        'username': users[1]
                    }
                  },
                  {
                    'node': {
                        'username': users[2]
                    }
                  },
                  {
                    'node': {
                        'username': users[3]
                    }
                  }
                ]
            }
        }
        response = self.client.post(self.endpoint, {'query': query}).json()
        self.assertEqual(expected, response['data'])

        # For descending ordering
        query = 'query {users(orderBy: "-%s") {edges{node{username}}}}' % (ordering_param)
        expected['users']['edges'].reverse()
        response = self.client.post(self.endpoint, {'query': query}).json()
        self.assertEqual(expected, response['data'])

    def test_api_endpoint_is_live(self):
        response = self.client.post(self.endpoint, {'query': ''})

        self.assertEqual(400, response.status_code)
        self.assertEqual(
            'Must provide query string.',
            response.json()['errors'][0]['message']
        )

    def test_creation_of_user_object(self):
        credentials = {
            'username': 'tom_dick',
            'password': 'qwerty123'
        }

        response = self.create_user(
            credentials['username'],
            credentials['password']
        )

        expected = {
            'createUser': {
                'user': {
                    'id': response['data']['createUser']['user']['id'],
                    'originalId': response['data']['createUser']['user']['originalId'],
                    'username': credentials['username']
                }
            }
        }

        self.assertEqual(expected, response['data'])

    def test_retrieval_of_one_user_object(self):
        expected = {
            'user': {
                'username': self.first_user['username']
            }
        }

        response = self.retrieve_user(self.first_user['id'])

        self.assertEqual(expected, response['data'])

    def test_retrieval_of_multiple_user_objects_without_filtering(self):
        new_users = self.create_multiple_users()

        query = 'query {users{edges{node{username}}}}'

        expected = {
            'users': {
                'edges': [
                  {
                    'node': {
                        'username': self.first_user['username']
                    }
                  },
                  {
                    'node': {
                        'username': new_users[0][0]
                    }
                  },
                  {
                    'node': {
                        'username': new_users[1][0]
                    }
                  },
                  {
                    'node': {
                        'username': new_users[2][0]
                    }
                  }
                ]
            }
        }

        response = self.client.post(self.endpoint, {'query': query}).json()

        self.assertEqual(expected, response['data'])

    def test_retrieval_of_multiple_user_objects_filter_by_username(self):
        new_users = self.create_multiple_users()

        query = 'query {users(username_Icontains: "H") {edges{node{username}}}}'

        expected = {
            'users': {
                'edges': [
                  {
                    'node': {
                        'username': new_users[0][0]
                    }
                  },
                  {
                    'node': {
                        'username': new_users[1][0]
                    }
                  }
                ]
            }
        }

        response = self.client.post(self.endpoint, {'query': query}).json()

        self.assertEqual(expected, response['data'])

    def test_retrieval_of_multiple_user_objects_filter_by_is_staff(self):
        self.create_multiple_users()

        query = 'query {users(isStaff: true) {edges{node{username}}}}'

        expected = {
            'users': {
                'edges': []
            }
        }

        response = self.client.post(self.endpoint, {'query': query}).json()

        self.assertEqual(expected, response['data'])

    def test_retrieval_of_multiple_user_objects_filter_by_is_active(self):
        self.create_multiple_users()

        query = 'query {users(isActive: true) {edges{node{username}}}}'

        expected = {
            'users': {
                'edges': []
            }
        }

        response = self.client.post(self.endpoint, {'query': query}).json()

        self.assertEqual(expected, response['data'])

    def test_retrieval_of_multiple_user_objects_ordering_by_id(self):
        new_users = self.create_multiple_users()
        users = [
            self.first_user['username'],
            new_users[0][0],
            new_users[1][0],
            new_users[2][0]
        ]

        self.ordering_test_helper('id', users)

    def test_retrieval_of_multiple_user_objects_ordering_by_username(self):
        new_users = self.create_multiple_users()
        users = [
            new_users[0][0],
            self.first_user['username'],
            new_users[1][0],
            new_users[2][0]
        ]

        self.ordering_test_helper('username', users)

    def test_retrieval_of_multiple_user_objects_ordering_by_date_joined(self):
        new_users = self.create_multiple_users()
        users = [
            self.first_user['username'],
            new_users[0][0],
            new_users[1][0],
            new_users[2][0]
        ]

        self.ordering_test_helper('date_joined', users)

    def test_update_of_user_object(self):
        query = '''
            mutation{
                updateUser(
                    input: {
                        id: "%s",
                        firstName: "Akeem",
                        lastName: "Oduola",
                        username: "oakeem",
                        email: "akeem.oduola@andela.com"
                    }
                )
                {
                    user{
                        id,
                        originalId,
                        username,
                        firstName,
                        lastName,
                        email
                    }
                }
            }
        ''' % (self.first_user['id'])

        expected = {
            "updateUser": {
                "user": {
                    "id": self.first_user['id'],
                    "originalId": self.first_user['originalId'],
                    "username": "oakeem",
                    "firstName": "Akeem",
                    "lastName": "Oduola",
                    "email": "akeem.oduola@andela.com",
                }
            }
        }

        response = self.client.post(self.endpoint, {'query': query}).json()

        self.assertEqual(expected, response['data'])

    def test_deletion_of_user_object(self):
        query = '''
            mutation{
                deleteUser(input: {id: "%s"}){
                    user{
                        username
                    }
                }
            }
        ''' % (self.first_user['id'])

        expected = {
            "deleteUser": {
                "user": {
                    "username": self.first_user['username']
                }
            }
        }

        response = self.client.post(self.endpoint, {'query': query}).json()
        self.assertEqual(expected, response['data'])

        response = self.retrieve_user(self.first_user['id'])
        self.assertEqual(None, response['data']['user'])
