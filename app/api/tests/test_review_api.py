from django.test import Client, TestCase

from app.timetables.factories import ServingFactory
from .utils import create_admin_account, make_request


class ReviewApiTest(TestCase):
    """Test for Review API."""

    def setUp(self):
        self.client = Client()
        create_admin_account()
        self.serving = ServingFactory()
        self.first_review = self.create_review(
            self.serving.public_id.hashid,
            3,
            'Fair meal'
        )['review']
        self.reviews = (
            (self.serving.public_id.hashid, 4, 'Good meal'),
            (self.serving.public_id.hashid, 5, 'Excellent meal')
        )

    def create_review(self, serving_public_id, value, comment):
        query = '''
                mutation{
                    createReview(input: {serving: "%s", value: "%s", comment: "%s"}){
                        review{
                            id,
                            originalId,
                            value,
                            comment,
                            serving{
                                publicId
                            }
                        }
                    }
                }
                ''' % (serving_public_id, value, comment)
        return make_request(self.client, query, 'POST')

    def retrieve_review(self, review_id):
        query = '''query {
                    review(id: "%s") {
                        id,
                        originalId,
                        value,
                        comment,
                        serving{
                            publicId
                        }
                    }
                }
                ''' % (review_id)

        return make_request(self.client, query)

    def create_multiple_reviews(self):
        return [self.create_review(public_id, value, comment)
                for public_id, value, comment in self.reviews]

    def test_creation_of_review_object(self):
        # For new review record
        response = self.create_review(self.serving.public_id.hashid, 1, 'Terrible meal')
        created_review = response['review']
        expected = {
            'review': {
                'id': created_review['id'],
                'originalId': created_review['originalId'],
                'value': 1,
                'comment': 'Terrible meal',
                'serving': {
                    'publicId': self.serving.public_id.hashid
                }
            }
        }
        self.assertEqual(expected, response)

    def test_retrieve_review_object(self):
        # Retrieve with valid id
        response = self.retrieve_review(self.first_review['id'])
        expected = {
            'review': {
                'id': self.first_review['id'],
                'originalId': self.first_review['originalId'],
                'value': self.first_review['value'],
                'comment': self.first_review['comment'],
                'serving': self.first_review['serving'],
            }
        }
        self.assertEqual(expected, response)

        # Retrieve with invalid id
        self.assertEqual({'review': None}, self.retrieve_review('jnejkndjkdyhwie'))

    def test_retrieve_multiple_reviews_without_filtering(self):
        self.create_multiple_reviews()

        query = 'query {reviews{edges{node{value,comment}}}}'

        expected = {
            'reviews': [
                {
                    'value': self.first_review['value'],
                    'comment': self.first_review['comment'],
                },
                {
                    'value': self.reviews[0][1],
                    'comment': self.reviews[0][2],
                },
                {
                    'value': self.reviews[1][1],
                    'comment': self.reviews[1][2],
                },
            ]
        }

        response = make_request(self.client, query)

        self.assertEqual(expected, response)

    def test_retrieve_multiple_reviews_filter_by_comment(self):
        self.create_multiple_reviews()
        query = 'query {reviews(comment_Icontains: "meal") {edges{node{value,comment}}}}'

        expected = {
            'reviews': [
                {
                    'value': self.first_review['value'],
                    'comment': self.first_review['comment'],
                },
                {
                    'value': self.reviews[0][1],
                    'comment': self.reviews[0][2],
                },
                {
                    'value': self.reviews[1][1],
                    'comment': self.reviews[1][2],
                },
            ]
        }

        response = make_request(self.client, query)

        self.assertEqual(expected, response)

    def test_update_review_object(self):
        # Update with valid id
        query = '''
            mutation{
                updateReview(
                    input: {
                        id: "%s",
                        value: "1"
                    }
                )
                {
                    review{
                        id,
                        originalId,
                        value,
                        comment,
                        serving{
                            publicId
                        }
                    }
                }
            }
        ''' % (self.first_review['id'])
        response = make_request(self.client, query, 'POST')
        expected = {
            'review': {
                'id': self.first_review['id'],
                'originalId': self.first_review['originalId'],
                'value': 1,
                'comment': self.first_review['comment'],
                'serving': self.first_review['serving'],
            }
        }
        self.assertEqual(expected, response)

        # Update with invalid id
        query = '''
            mutation{
                updateReview(
                    input: {
                        id: "%s",
                        value: "1"
                    }
                )
                {
                    review{
                        id,
                        originalId,
                        value,
                        comment,
                        serving{
                            publicId
                        }
                    }
                }
            }
        ''' % ('hbhjbjkbijhiehokdj')
        self.assertEqual({'review': None},
                         make_request(self.client, query, 'POST'))

    def test_deletion_review_object(self):
        # Delete with valid id
        query = '''
            mutation{
                deleteReview(input: {id: "%s"}){
                    review{
                        value,
                        comment
                    }
                }
            }
        ''' % (self.first_review['id'])
        response = make_request(self.client, query, 'POST')
        expected = {
            'review': {
                'value': self.first_review['value'],
                'comment': self.first_review['comment'],
            }
        }
        self.assertEqual(expected, response)
        self.assertEqual({'review': None}, self.retrieve_review(self.first_review['id']))

        # Delete with invalid id
        query = '''
            mutation{
                deleteReview(input: {id: "%s"}){
                    review{
                        value,
                        comment
                    }
                }
            }
        ''' % ('jjjkhfihokjojf')
        self.assertEqual({'review': None}, make_request(self.client, query, 'POST'))
