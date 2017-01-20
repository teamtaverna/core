from base64 import b64encode

from django.contrib.auth.models import User
from django.test import Client, TestCase

from ..models import ApiKey


class ApiViewTest(TestCase):
    """Test for API Views."""

    def setUp(self):
        self.client = Client()
        self.user_test_credentials = ('user1', 'user1@taverna.com', 'qwerty123')
        self.admin_test_credentials = ('admin', 'admin@taverna.com', 'qwerty123')
        self.create_user_account()
        self.create_admin_account()

    @classmethod
    def b64encode_credentials(cls, username, password):
        credentials = '{}:{}'.format(username, password)
        b64_encoded_credentials = b64encode(credentials.encode('utf-8'))

        return b64_encoded_credentials.decode('utf-8')

    def create_user_account(self):
        User.objects.create_user(*self.user_test_credentials)

    def create_admin_account(self):
        User.objects.create_superuser(*self.admin_test_credentials)

    def test_api_key_issuance_handler(self):
        endpoint = '/api/api_key'

        # POST Request without Authorization header
        response = self.client.post(endpoint).json()
        self.assertEqual(
            'Use Basic Auth and supply your username and password.',
            response['message']
        )

        # POST Request with invalid Authorization header
        response = self.client.post(
            endpoint,
            **{'HTTP_AUTHORIZATION': 'YWRtaW46a25pZ2h0MTg='}
        ).json()
        self.assertEqual(
            'Use Basic Auth and supply your username and password.',
            response['message']
        )

        # POST Request with invalid credentials
        response = self.client.post(
            endpoint,
            **{'HTTP_AUTHORIZATION': 'Basic %s' % self.b64encode_credentials('support', 'qwerty')}
        ).json()
        self.assertEqual('Invalid Credentials.', response['message'])

        # POST Request with normal user credentials
        uname, email, passwd = self.user_test_credentials
        response = self.client.post(
            endpoint,
            **{'HTTP_AUTHORIZATION': 'Basic %s' % self.b64encode_credentials(uname, passwd)}
        ).json()
        self.assertEqual('Unauthorized.', response['message'])

        # POST Request with admin user credentials
        uname, email, passwd = self.admin_test_credentials
        response = self.client.post(
            endpoint,
            **{'HTTP_AUTHORIZATION': 'Basic %s' % self.b64encode_credentials(uname, passwd)}
        ).json()
        issued_api_key = ApiKey.objects.get(owner__username=uname, revoked=False)
        self.assertEqual(issued_api_key.token.hashid, response['api_key'])

        # POST Request with url ending with api_key
        response = self.client.post(
            '%s/%s' % (endpoint, response['api_key']),
            **{'HTTP_AUTHORIZATION': 'Basic %s' % self.b64encode_credentials(uname, passwd)}
        ).json()
        self.assertEqual('Bad Request.', response['message'])

    def test_api_key_revocation_handler(self):
        admin = User.objects.get(username='admin')
        api_key = ApiKey.objects.create(owner=admin, revoked=False)
        endpoint_without_token = '/api/api_key'
        endpoint = '%s/%s' % (endpoint_without_token, api_key.token.hashid)

        # DELETE Request without Authorization header
        response = self.client.delete(endpoint).json()
        self.assertEqual(
            'Use Basic Auth and supply your username and password.',
            response['message']
        )

        # DELETE Request with invalid Authorization header
        response = self.client.delete(
            endpoint,
            **{'HTTP_AUTHORIZATION': 'YWRtaW46a25pZ2h0MTg='}
        ).json()
        self.assertEqual(
            'Use Basic Auth and supply your username and password.',
            response['message']
        )

        # DELETE Request with invalid credentials
        response = self.client.delete(
            endpoint,
            **{'HTTP_AUTHORIZATION': 'Basic %s' % self.b64encode_credentials('support', 'qwerty')}
        ).json()
        self.assertEqual('Invalid Credentials.', response['message'])

        # DELETE Request with admin user credentials
        uname, email, passwd = self.admin_test_credentials
        response = self.client.delete(
            endpoint,
            **{'HTTP_AUTHORIZATION': 'Basic %s' % self.b64encode_credentials(uname, passwd)}
        ).json()
        self.assertEqual('%s was revoked.' % api_key.token.hashid, response['message'])

        # DELETE Request with invalid api_key
        response = self.client.delete(
            '%s/%s' % (endpoint_without_token, 'a49d7536849be9da859a67bae2d7256e'),
            **{'HTTP_AUTHORIZATION': 'Basic %s' % self.b64encode_credentials(uname, passwd)}
        ).json()
        self.assertEqual('Bad Request.', response['message'])

        # DELETE Request with url without api_key
        response = self.client.delete(
            endpoint_without_token,
            **{'HTTP_AUTHORIZATION': 'Basic %s' % self.b64encode_credentials(uname, passwd)}
        ).json()
        self.assertEqual('Bad Request.', response['message'])
