from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase

from ..models import ApiKey

class ApiKeyTest(TestCase):
    """Tests the ApiKey model."""

    def test_only_superuser_can_create_api_key(self):
        # Using normal users.
        normal_user = User.objects.create_user('user1', 'user1@taverna.com', 'qwerty123')
        self.assertRaises(ValidationError, ApiKey.objects.create, owner=normal_user)

        # Using super users.
        super_user = User.objects.create_superuser('admin', 'admin@taverna.com', 'qwerty123')
        api_key = ApiKey.objects.create(owner=super_user)
        self.assertIsInstance(api_key, ApiKey)
