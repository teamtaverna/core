from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    """
    Models extra information about users that are not built into Django's default user model.

    Example of extra information can be google user id, facebook user id, etc.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    custom_auth_id = models.CharField(max_length=255, blank=True)
    facebook_oauth_id = models.CharField(max_length=255, blank=True)
    google_oauth_id = models.CharField(max_length=255, blank=True)
    twitter_oauth_id = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.user.username
