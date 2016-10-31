from django.test import Client, TestCase


class ApiTest(TestCase):
    """Test for API"""

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
