from __future__ import unicode_literals

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _


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
            slugify_field_value = getattr(self, self.slugify_field)
            self.slug = slugify(slugify_field_value)

            # If pk exists, object exists in db and is being edited by user.
            if self.__class__.objects.filter(slug=self.slug).exists() and not self.pk:
                raise ValidationError(_("Entry with {0} - {1} already exists.".format(
                                        self.slugify_field, slugify_field_value)))

    def save(self, *args, **kwargs):
        self.clean()
        return super().save(*args, **kwargs)
