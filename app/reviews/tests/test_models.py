from django.db.utils import IntegrityError
from django.test import TestCase

from app.reviews.factories import ReviewFactory
from app.reviews.models import Review


class ReviewTest(TestCase):
    """Test the Review model."""

    def setUp(self):
        self.review = ReviewFactory()

    def test_enforcement_of_one_review_per_serviving_per_user(self):
        review_new = Review(
            user=self.review.user,
            serving=self.review.serving,
            value=2,
            comment=''
        )

        self.assertRaises(IntegrityError, review_new.save)
