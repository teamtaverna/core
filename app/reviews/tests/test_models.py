from django.core.exceptions import ValidationError
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

        self.assertRaises(ValidationError, review_new.save)

    def test_enforcement_of_one_review_per_serviving_per_anonymous_user(self):
        review_new = Review(
            anonymity_id=self.review.anonymity_id,
            serving=self.review.serving,
            value=2,
            comment=''
        )

        self.assertRaises(ValidationError, review_new.save)

    def test_multiple_reviews_without_user_and_anonymity_id(self):
        review_one = Review.objects.create(
            serving=self.review.serving,
            value=2,
            comment=''
        )

        review_two = Review.objects.create(
            serving=self.review.serving,
            value=2,
            comment=''
        )

        reviews = Review.objects.all()
        self.assertIn(review_one, reviews)
        self.assertIn(review_two, reviews)
