import factory

from . import models
from app.timetables.factories import ServingFactory, TimestampFactory, UserFactory


class ReviewFactory(TimestampFactory):
    """Review model factory."""

    class Meta:
        model = models.Review

    user = factory.SubFactory(UserFactory)
    serving = factory.SubFactory(ServingFactory)
    value = 4
    comment = 'Fresh and Delicious!'
