from django.core.exceptions import ValidationError
from django.test import TestCase

from ..models import ApiKey
from .utils import create_admin_account, create_normal_user_acount


class ApiKeyTest(TestCase):
    """Tests the ApiKey model."""

    def test_api_key_creation_using_normal_users(self):
        normal_user = create_normal_user_acount()

        self.assertRaises(ValidationError, ApiKey.objects.create, owner=normal_user)

    def test_api_key_creation_using_super_users(self):
        super_user = create_admin_account()
        api_key = ApiKey.objects.create(owner=super_user)

        self.assertIsInstance(api_key, ApiKey)
