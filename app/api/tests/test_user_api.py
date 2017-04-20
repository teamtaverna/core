from django.test import Client, TestCase

from .utils import (admin_test_credentials, create_admin_account,
                    make_request,)


class UserApiTest(TestCase):
    """Test for User API"""

    def setUp(self):
        self.client = Client()
        create_admin_account()
        self.first_user = self.create_user('oakeem', 'oatman')['user']

    def create_user(self, username, password):
        query = '''
            mutation{
              createUser(input: {user:{username: "%s", password: "%s"}}){
                user{
                  id,
                  originalId,
                  username
                }
              }
            }
        ''' % (username, password)

        return make_request(self.client, query, 'POST')

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

        return make_request(self.client, query)

    def ordering_test_helper(self, ordering_param, users):
        # For ascending ordering
        query = 'query{users(orderBy: "%s") {edges{node{username}}}}' % (ordering_param)
        expected = {
            'users': [
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
        }
        self.assertEqual(expected, make_request(self.client, query))

        # For descending ordering
        query = 'query {users(orderBy: "-%s") {edges{node{username}}}}' % (ordering_param)
        expected['users'].reverse()
        self.assertEqual(expected, make_request(self.client, query))

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
        created_user = response['user']
        expected = {
            'user': {
                'id': created_user['id'],
                'originalId': created_user['originalId'],
                'username': created_user['username']
            }
        }
        self.assertEqual(expected, response)

        # For existing user record
        response = self.create_user(
            credentials['username'],
            credentials['password']
        )
        self.assertEqual({'user': None}, response)

    def test_creation_of_user_with_profile(self):
        query = '''
            mutation{
              createUser(input: {user:{username: "%s", password: "%s"},
                profile: {customAuthId:"abc"}}){
                user{
                  id,
                  originalId,
                  username,
                  profile{customAuthId}
                }
              }
            }
        ''' % ('tom_dick', 'qwerty123')

        response = self.make_request(query, 'POST')
        created_user = response['user']
        expected = {
            'user': {
                'id': created_user['id'],
                'originalId': created_user['originalId'],
                'username': created_user['username'],
                'profile': {'customAuthId': 'abc'}
            }
        }
        self.assertEqual(expected, response)

    def test_retrieval_of_one_user_object(self):
        # Retrieve with valid id
        expected = {
            'user': {
                'username': self.first_user['username']
            }
        }
        self.assertEqual(expected, self.retrieve_user(self.first_user['id']))

        # Retrieve with invalid id
        self.assertEqual({'user': None}, self.retrieve_user(100))

    def test_retrieval_of_multiple_user_objects_without_filtering(self):
        new_users = self.create_multiple_users()

        query = 'query {users{edges{node{username}}}}'

        expected = {
           'users': [
                {
                    'username': admin_test_credentials[0]
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
        }

        self.assertEqual(expected, make_request(self.client, query))

    def test_retrieval_of_multiple_user_objects_filter_by_username(self):
        new_users = self.create_multiple_users()

        query = 'query {users(username_Icontains: "H") {edges{node{username}}}}'

        expected = {
            'users': [
                {
                    'username': new_users[0][0]
                },
                {
                    'username': new_users[1][0]
                }
            ]
        }

        self.assertEqual(expected, make_request(self.client, query))

    def test_retrieval_of_multiple_user_objects_filter_by_is_staff(self):
        self.create_multiple_users()

        query = 'query {users(isStaff: true) {edges{node{username}}}}'

        expected = {
            'users': [
                {
                    'username': admin_test_credentials[0]
                }
            ]
        }

        self.assertEqual(expected, make_request(self.client, query))

    def test_retrieval_of_multiple_user_objects_filter_by_is_active(self):
        self.create_multiple_users()

        query = 'query {users(isActive: true) {edges{node{username}}}}'

        expected = {
            'users': [
                {
                    'username': admin_test_credentials[0]
                }
            ]
        }

        self.assertEqual(expected, make_request(self.client, query))

    def test_retrieval_of_multiple_user_objects_ordering_by_id(self):
        new_users = self.create_multiple_users()
        users = [
            admin_test_credentials[0],
            self.first_user['username'],
            new_users[0][0],
            new_users[1][0],
            new_users[2][0]
        ]

        self.ordering_test_helper('id', users)

    def test_retrieval_of_multiple_user_objects_ordering_by_username(self):
        new_users = self.create_multiple_users()
        users = [
            admin_test_credentials[0],
            new_users[0][0],
            self.first_user['username'],
            new_users[1][0],
            new_users[2][0]
        ]

        self.ordering_test_helper('username', users)

    def test_retrieval_of_multiple_user_objects_ordering_by_date_joined(self):
        new_users = self.create_multiple_users()
        users = [
            admin_test_credentials[0],
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
                        user:{
                            id: "%s",
                            firstName: "Akeem",
                            lastName: "Oduola",
                            username: "oakeem",
                            email: "akeem.oduola@andela.com"
                        }

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
            'user': {
                'id': self.first_user['id'],
                'originalId': self.first_user['originalId'],
                'username': 'oakeem',
                'firstName': 'Akeem',
                'lastName': 'Oduola',
                'email': 'akeem.oduola@andela.com',
            }
        }

        self.assertEqual(expected, make_request(self.client, query, 'POST'))

        # Update with invalid id
        query = '''
            mutation{
                updateUser(
                    input: {
                        user:{
                            id: "%s",
                            firstName: "Akeem",
                            lastName: "Oduola",
                            username: "oakeem",
                            email: "akeem.oduola@andela.com"
                        }
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
        self.assertEqual({'user': None}, make_request(self.client, query, 'POST'))

    def test_update_of_user_object_with_profile(self):
        # Update with valid id
        query = '''
            mutation{
                updateUser(
                    input: {
                        user:{
                            id: "%s",
                            firstName: "Akeem",
                            lastName: "Oduola",
                            username: "oakeem",
                            email: "akeem.oduola@andela.com"
                        },
                        profile: {customAuthId:"abcd"}

                    }
                )
                {
                    user{
                        id,
                        originalId,
                        username,
                        firstName,
                        lastName,
                        email,
                        profile{customAuthId}
                    }
                }
            }
        ''' % (self.first_user['id'])

        expected = {
            'user': {
                'id': self.first_user['id'],
                'originalId': self.first_user['originalId'],
                'username': 'oakeem',
                'firstName': 'Akeem',
                'lastName': 'Oduola',
                'email': 'akeem.oduola@andela.com',
                'profile': {
                    'customAuthId': 'abcd'
                }
            }
        }

        self.assertEqual(expected, self.make_request(query, 'POST'))

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
            'user': {
                'username': self.first_user['username']
            }
        }

        self.assertEqual(expected, make_request(self.client, query, 'POST'))
        self.assertEqual({'user': None}, self.retrieve_user(self.first_user['id']))

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
        self.assertEqual({'user': None}, make_request(self.client, query, 'POST'))
