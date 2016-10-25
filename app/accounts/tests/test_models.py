from django.db import IntegrityError
from django.test import TestCase

from app.accounts.models import UserProfile
from app.timetables.factories import UserFactory


class UserProfileTest(TestCase):
    """Test UserProfile model"""

    def setUp(self):
        self.user = UserFactory()

    def test_user_can_only_have_one_profile_entry(self):
        profile = UserProfile(user=self.user, custom_auth_id='134664323567')
        self.assertRaises(IntegrityError, profile.save)

    def test_profile_is_created_on_user_creation(self):
        user_profile = UserProfile.objects.get(user=self.user)
        self.assertEqual(user_profile.user, self.user)
