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
        self.api_key = self.create_api_key()
        self.api_key_issuance_endpoint = '/api/api_key'
        self.api_key_revocation_endpoint = '{}/{}'.format(
            self.api_key_issuance_endpoint,
            self.api_key
        )

    @classmethod
    def b64encode_credentials(cls, username, password):
        credentials = '{}:{}'.format(username, password)
        b64_encoded_credentials = b64encode(credentials.encode('utf-8'))

        return b64_encoded_credentials.decode('utf-8')

    def create_user_account(self):
        User.objects.create_user(*self.user_test_credentials)

    def create_admin_account(self):
        User.objects.create_superuser(*self.admin_test_credentials)

    def create_api_key(self):
        uname, email, passwd = self.admin_test_credentials
        admin = User.objects.get(username=uname)

        return ApiKey.objects.create(owner=admin, revoked=False).token.hashid

    def test_api_key_issuance_handler_without_authorization_header(self):
        response = self.client.post(self.api_key_issuance_endpoint).json()

        self.assertEqual(
            'Use Basic Auth and supply your username and password.',
            response['message']
        )

    def test_api_key_issuance_handler_with_invalid_authorization_header(self):
        response = self.client.post(
            self.api_key_issuance_endpoint,
            **{'HTTP_AUTHORIZATION': 'YWRtaW46a25pZ2h0MTg='}
        ).json()

        self.assertEqual(
            'Use Basic Auth and supply your username and password.',
            response['message']
        )

    def test_api_key_issuance_handler_with_invalid_credentials(self):
        response = self.client.post(
            self.api_key_issuance_endpoint,
            **{'HTTP_AUTHORIZATION': 'Basic {}'.format(
                self.b64encode_credentials('support', 'qwerty')
            )}
        ).json()

        self.assertEqual('Invalid Credentials.', response['message'])

    def test_api_key_issuance_handler_with_normal_user_credentials(self):
        uname, email, passwd = self.user_test_credentials
        response = self.client.post(
            self.api_key_issuance_endpoint,
            **{'HTTP_AUTHORIZATION': 'Basic {}'.format(self.b64encode_credentials(uname, passwd))}
        ).json()

        self.assertEqual('Unauthorized.', response['message'])

    def test_api_key_issuance_handler_with_admin_user_credentials(self):
        uname, email, passwd = self.admin_test_credentials
        response = self.client.post(
            self.api_key_issuance_endpoint,
            **{'HTTP_AUTHORIZATION': 'Basic {}'.format(self.b64encode_credentials(uname, passwd))}
        ).json()
        issued_api_key = ApiKey.objects.get(owner__username=uname, revoked=False)

        self.assertEqual(issued_api_key.token.hashid, response['api_key'])

    def test_api_key_issuance_handler_with_url_ending_with_api_key(self):
        uname, email, passwd = self.admin_test_credentials
        response = self.client.post(
            self.api_key_revocation_endpoint,
            **{'HTTP_AUTHORIZATION': 'Basic {}'.format(self.b64encode_credentials(uname, passwd))}
        ).json()

        self.assertEqual('Bad Request.', response['message'])

    def test_api_key_revocation_handler_without_authorization_header(self):
        response = self.client.delete(self.api_key_revocation_endpoint).json()

        self.assertEqual(
            'Use Basic Auth and supply your username and password.',
            response['message']
        )

    def test_api_key_revocation_handler_with_invalid_authorization_header(self):
        response = self.client.delete(
            self.api_key_revocation_endpoint,
            **{'HTTP_AUTHORIZATION': 'YWRtaW46a25pZ2h0MTg='}
        ).json()
        self.assertEqual(
            'Use Basic Auth and supply your username and password.',
            response['message']
        )

    def test_api_key_revocation_handler_with_invalid_credentials(self):
        response = self.client.delete(
            self.api_key_revocation_endpoint,
            **{'HTTP_AUTHORIZATION': 'Basic {}'.format(
                self.b64encode_credentials('support', 'qwerty')
            )}
        ).json()

        self.assertEqual('Invalid Credentials.', response['message'])

    def test_api_key_revocation_handler_with_admin_user_credentials(self):
        uname, email, passwd = self.admin_test_credentials
        response = self.client.delete(
            self.api_key_revocation_endpoint,
            **{'HTTP_AUTHORIZATION': 'Basic {}'.format(self.b64encode_credentials(uname, passwd))}
        ).json()

        self.assertEqual('%s was revoked.' % self.api_key, response['message'])

    def test_api_key_revocation_handler_with_invalid_api_key(self):
        uname, email, passwd = self.admin_test_credentials
        response = self.client.delete(
            '%s/%s' % (self.api_key_issuance_endpoint, 'a49d7536849be9da859a67bae2d7256e'),
            **{'HTTP_AUTHORIZATION': 'Basic {}'.format(self.b64encode_credentials(uname, passwd))}
        ).json()

        self.assertEqual('Bad Request.', response['message'])

    def test_api_key_revocation_handler_with_url_without_api_key(self):
        uname, email, passwd = self.admin_test_credentials
        response = self.client.delete(
            self.api_key_issuance_endpoint,
            **{'HTTP_AUTHORIZATION': 'Basic {}'.format(self.b64encode_credentials(uname, passwd))}
        ).json()

        self.assertEqual('Bad Request.', response['message'])
