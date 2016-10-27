from django.test import Client, TestCase


class ApiTest(TestCase):
    """Test for API"""

    def setUp(self):
        self.client = Client()
        self.endpoint = '/api'

    def test_api_endpoint_is_live(self):
        r = self.client.get(self.endpoint, {'query': ''})

        self.assertEqual(400, r.status_code)
        self.assertEqual('Must provide query string.', r.json()['errors'][0]['message'])
