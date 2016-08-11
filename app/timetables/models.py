from __future__ import unicode_literals

from django.db import models

from app.shared.models import CommonInfo


class Course(CommonInfo):
    name = models.CharField(max_length=150, unique=True)

    def __str(self):
        return self.name
