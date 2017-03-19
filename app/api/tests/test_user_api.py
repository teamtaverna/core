from django.test import Client, TestCase

from .utils import obtain_api_key, create_admin_account


class UserApiTest(TestCase):
    """Test for User API"""

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
        self.first_user = self.create_user('oakeem', 'oatman')

    def make_request(self, query, method='GET'):
        if method == 'GET':
            return self.client.get(self.endpoint, data={'query': query}, **self.header).json()

        if method == 'POST':
            return self.client.post(self.endpoint, data={'query': query}, **self.header).json()

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

        return self.make_request(query, 'POST')

    def create_multiple_users(self):
        new_users = (
            ('john', 'qwerty123'),
            ('raphael', 'qwerty123'),
            ('samson', 'qwerty123'),
        )

        [self.create_user(username, password) for username, password in new_users]

        return new_users

    def retrieve_user(self, user_id):
        query = 'query {user(id: "%s") {username}}' % (user_id)

        return self.make_request(query)

    def ordering_test_helper(self, ordering_param, users):
        # For ascending ordering
        query = 'query{users(orderBy: "%s") {edges{node{username}}}}' % (ordering_param)
        expected = [
            {
                'username': users[0]
            },
            {
                'username': users[1]
            },
            {
                'username': users[2]
            },
            {
                'username': users[3]
            },
            {
                'username': users[4]
            }
        ]
        self.assertEqual(expected, self.make_request(query))

        # For descending ordering
        query = 'query {users(orderBy: "-%s") {edges{node{username}}}}' % (ordering_param)
        expected.reverse()
        self.assertEqual(expected, self.make_request(query))

    def test_creation_of_user_object(self):
        credentials = {
            'username': 'tom_dick',
            'password': 'qwerty123'
        }

        # For new user record
        response = self.create_user(
            credentials['username'],
            credentials['password']
        )
        expected = {
            'id': response['id'],
            'originalId': response['originalId'],
            'username': credentials['username']
        }
        self.assertEqual(expected, response)

        # For existing user record
        response = self.create_user(
            credentials['username'],
            credentials['password']
        )
        self.assertEqual(None, response)

    def test_retrieval_of_one_user_object(self):
        # Retrieve with valid id
        expected = {
            'username': self.first_user['username']
        }
        self.assertEqual(expected, self.retrieve_user(self.first_user['id']))

        # Retrieve with invalid id
        self.assertEqual(None, self.retrieve_user(100))

    def test_retrieval_of_multiple_user_objects_without_filtering(self):
        new_users = self.create_multiple_users()

        query = 'query {users{edges{node{username}}}}'

        expected = [
            {
                'username': self.admin_test_credentials[0]
            },
            {
                'username': self.first_user['username']
            },
            {
                'username': new_users[0][0]
            },
            {
                'username': new_users[1][0]
            },
            {
                'username': new_users[2][0]
            }
        ]

        self.assertEqual(expected, self.make_request(query))

    def test_retrieval_of_multiple_user_objects_filter_by_username(self):
        new_users = self.create_multiple_users()

        query = 'query {users(username_Icontains: "H") {edges{node{username}}}}'

        expected = [
            {
                'username': new_users[0][0]
            },
            {
                'username': new_users[1][0]
            }
        ]

        self.assertEqual(expected, self.make_request(query))

    def test_retrieval_of_multiple_user_objects_filter_by_is_staff(self):
        self.create_multiple_users()

        query = 'query {users(isStaff: true) {edges{node{username}}}}'

        expected = [
            {
                'username': self.admin_test_credentials[0]
            }
        ]

        self.assertEqual(expected, self.make_request(query))

    def test_retrieval_of_multiple_user_objects_filter_by_is_active(self):
        self.create_multiple_users()

        query = 'query {users(isActive: true) {edges{node{username}}}}'

        expected = [
            {
                'username': self.admin_test_credentials[0]
            }
        ]

        self.assertEqual(expected, self.make_request(query))

    def test_retrieval_of_multiple_user_objects_ordering_by_id(self):
        new_users = self.create_multiple_users()
        users = [
            self.admin_test_credentials[0],
            self.first_user['username'],
            new_users[0][0],
            new_users[1][0],
            new_users[2][0]
        ]

        self.ordering_test_helper('id', users)

    def test_retrieval_of_multiple_user_objects_ordering_by_username(self):
        new_users = self.create_multiple_users()
        users = [
            self.admin_test_credentials[0],
            new_users[0][0],
            self.first_user['username'],
            new_users[1][0],
            new_users[2][0]
        ]

        self.ordering_test_helper('username', users)

    def test_retrieval_of_multiple_user_objects_ordering_by_date_joined(self):
        new_users = self.create_multiple_users()
        users = [
            self.admin_test_credentials[0],
            self.first_user['username'],
            new_users[0][0],
            new_users[1][0],
            new_users[2][0]
        ]

        self.ordering_test_helper('date_joined', users)

    def test_update_of_user_object(self):
        # Update with valid id
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
            'id': self.first_user['id'],
            'originalId': self.first_user['originalId'],
            'username': 'oakeem',
            'firstName': 'Akeem',
            'lastName': 'Oduola',
            'email': 'akeem.oduola@andela.com',
        }

        self.assertEqual(expected, self.make_request(query, 'POST'))

        # Update with invalid id
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
        ''' % ('wrong-id')
        self.assertEqual(None, self.make_request(query, 'POST'))

    def test_deletion_of_user_object(self):
        # Delete with valid id
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
            'username': self.first_user['username']
        }

        self.assertEqual(expected, self.make_request(query, 'POST'))
        self.assertEqual(None, self.retrieve_user(self.first_user['id']))

        # Delete with invalid id
        query = '''
            mutation{
                deleteUser(input: {id: "%s"}){
                    user{
                        username
                    }
                }
            }
        ''' % ('wrong-id')
        self.assertEqual(None, self.make_request(query, 'POST'))
