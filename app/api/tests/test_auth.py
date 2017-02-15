from base64 import b64encode
import json

from django.contrib.auth.models import User
from django.http import HttpRequest, JsonResponse
from django.test import Client, TestCase

from ..auth import authorization_required


class ApiAuthTest(TestCase):
    """Test for API Auth."""

    def setUp(self):
        self.request = HttpRequest()
        self.admin_test_credentials = ('admin', 'admin@taverna.com', 'qwerty123')

    def obtain_api_key(self):
        client = Client()
        credentials = '{}:{}'.format(
            self.admin_test_credentials[0],
            self.admin_test_credentials[2]
        )
        b64_encoded_credentials = b64encode(credentials.encode('utf-8'))

        return client.post(
            '/api/api_key',
            **{'HTTP_AUTHORIZATION': 'Basic %s' % b64_encoded_credentials.decode('utf-8')}
        ).json()['api_key']

    def create_admin_account(self):
        User.objects.create_superuser(*self.admin_test_credentials)

    @staticmethod
    @authorization_required
    def sample_view(request):
        return JsonResponse({'message': 'Success.'})

    def make_request(self):
        response = self.sample_view(self.request)
        return json.loads(response.content.decode('utf-8'))

    def test_api_get_request_without_api_key_header(self):
        self.request.method = 'GET'
        response = self.make_request()

        self.assertEqual('Set your api_key in X-TavernaToken header.', response['message'])

    def test_api_get_request_with_invalid_api_key_header(self):
        self.request.method = 'GET'
        self.request.META['HTTP_X_TAVERNATOKEN'] = 'a49d7536849be9da859a67bae2d7256f'
        response = self.make_request()

        self.assertEqual('Invalid Token.', response['message'])

    def test_api_get_request_with_valid_api_key_header(self):
        self.request.method = 'GET'
        self.create_admin_account()
        self.request.META['HTTP_X_TAVERNATOKEN'] = self.obtain_api_key()
        response = self.make_request()

        self.assertEqual('Success.', response['message'])

    def test_api_post_request_without_api_key_header(self):
        self.request.method = 'POST'
        response = self.make_request()

        self.assertEqual('Set your api_key in X-TavernaToken header.', response['message'])

    def test_api_post_request_with_invalid_api_key_header(self):
        self.request.method = 'POST'
        self.request.META['HTTP_X_TAVERNATOKEN'] = 'a49d7536849be9da859a67bae2d7256f'
        response = self.make_request()

        self.assertEqual('Invalid Token.', response['message'])

    def test_api_post_request_with_valid_api_key_header(self):
        self.request.method = 'POST'
        self.create_admin_account()
        self.request.META['HTTP_X_TAVERNATOKEN'] = self.obtain_api_key()
        response = self.make_request()

        self.assertEqual('Success.', response['message'])
