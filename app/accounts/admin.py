from django.contrib import admin

from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    fieldsets = [
        ('User Profile', {
            'fields': ('user', 'custom_auth_id', 'facebook_oauth_id',
                       'google_oauth_id', 'twitter_oauth_id',),
            'description': 'This holds extra optional information about admin users.'
        }),
    ]
