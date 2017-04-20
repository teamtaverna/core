import json

from django.http import HttpRequest, JsonResponse
from django.test import Client, TestCase

from ..auth import authorization_required
from .utils import obtain_api_key, create_admin_account


class ApiAuthTest(TestCase):
    """Test for API Auth."""

    def setUp(self):
        self.client = Client()
        self.request = HttpRequest()

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
        create_admin_account()
        self.request.META['HTTP_X_TAVERNATOKEN'] = obtain_api_key(self.client)
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
        create_admin_account()
        self.request.META['HTTP_X_TAVERNATOKEN'] = obtain_api_key(self.client)
        response = self.make_request()

        self.assertEqual('Success.', response['message'])
