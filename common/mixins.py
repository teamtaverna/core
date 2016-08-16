from __future__ import unicode_literals

from django.db import models


class TimestampMixin(models.Model):
    """Mixin for date and timestamp. Inherits django's models.Model."""

    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ForceCapitalizeMixin():
    """Capitalize the first letter of the model fields specified."""

    def clean(self):
        if hasattr(self, 'capitalized_field_names'):
            for field_name in self.capitalized_field_names:
                self.__dict__[field_name] = self.__dict__[field_name].capitalize()
                # ToDO: Do a check to ensure that only capitalizable fields
                # (TextField and CharField) are capitalized.

    def save(self, *args, **kwargs):
        self.clean()
        return super().save(*args, **kwargs)
