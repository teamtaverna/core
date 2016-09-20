from __future__ import unicode_literals

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import slugify


class TimestampMixin(models.Model):
    """Mixin for date and timestamp. Inherits django's models.Model."""

    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SlugifyMixin():
    """
    Slugify specific field and pass as value to slug field in the model.

    This mixin helps in solving the problem of having case insensitive duplicates
    by creating a slug and ensuring uniqueness.
    Model field to be slugified should be passed as a string into a variable
    called slugify_field.
    Slug field in the model should be named slug.
    """

    def clean(self):
        if hasattr(self, 'slugify_field') and hasattr(self, 'slug'):
            self.slug = slugify(getattr(self, self.slugify_field))

            if self.__class__.objects.filter(slug=self.slug).exists():
                raise ValidationError("This object already exists.")

    def save(self, *args, **kwargs):
        self.clean()
        return super().save(*args, **kwargs)
