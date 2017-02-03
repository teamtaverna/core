from django.contrib import admin

from .models import ApiKey


@admin.register(ApiKey)
class ApiKeyAdmin(admin.ModelAdmin):
    """Admin customisation for ApiKey model."""

    readonly_fields = ('token', 'date_created', 'date_modified')
    fields = (
        'token', 'revoked', 'owner', 'date_created', 'date_modified'
    )
