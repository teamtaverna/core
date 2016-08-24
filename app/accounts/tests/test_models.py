from django.contrib.auth.models import User
from django.db import IntegrityError
from django.test import TestCase

from app.accounts.models import UserProfile


class UserProfileTest(TestCase):
    """Test UserProfile model"""

    def setUp(self):
        self.user = User.objects.create(username='frank', password='secret')
        UserProfile.objects.create(user=self.user)

    def test_user_can_only_have_one_profile_entry(self):
        profile = UserProfile(user=self.user, custom_auth_id='134664323567')

        self.assertRaises(IntegrityError, profile.save)
