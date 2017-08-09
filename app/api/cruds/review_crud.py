from django.core.exceptions import ValidationError

import graphene
from graphene_django import DjangoObjectType
from django_filters import OrderingFilter, FilterSet

from app.reviews.models import Review
from app.timetables.models import Serving
from .utils import get_errors, get_object, load_object


class ReviewFilter(FilterSet):

    order_by = OrderingFilter(fields=[('value', 'value')])

    class Meta:
        fields = {'value': ['exact'], 'comment': ['icontains']}
        model = Review


class ReviewNode(DjangoObjectType):
    """API functionality for review model. """

    original_id = graphene.Int()
    value = graphene.Int()

    class Meta:
        model = Review
        interfaces = (graphene.relay.Node,)

    def resolve_original_id(self, args, context, info):
        return self.id


class CreateReview(graphene.relay.ClientIDMutation):
    """API functionality to create reviews."""

    review = graphene.Field(ReviewNode)
    errors = graphene.List(graphene.String)

    class Input:
        serving = graphene.String(required=True)
        value = graphene.String(required=True)
        comment = graphene.String(required=False)
        anonymity_id = graphene.String(required=False)

    @classmethod
    def mutate_and_get_payload(cls, args, context, info):
        try:
            review = Review(
                serving=Serving.objects.get(public_id=args.get('serving')),
                value=int(args.get('value')),
                comment=args.get('comment', ''),
                anonymity_id=args.get('anonymity_id', ''),
            )
            review.full_clean()
            review.save()
            return cls(review=review)
        except ValidationError as e:
            return cls(review=None, errors=get_errors(e))


class UpdateReview(graphene.relay.ClientIDMutation):
    """API functionality to update reviews."""

    review = graphene.Field(ReviewNode)
    errors = graphene.List(graphene.String)

    class Input:
        id = graphene.String(required=True)
        value = graphene.String(required=True)
        comment = graphene.String(required=False)

    @classmethod
    def mutate_and_get_payload(cls, args, context, info):
        review = get_object(Review, args.get('id'))
        review = load_object(review, args)
        try:
            if review:
                review.full_clean()
                review.save()
            return cls(review=review)
        except ValidationError as e:
            return cls(review=review, errors=get_errors(e))


class DeleteReview(graphene.relay.ClientIDMutation):
    """API functionality to delete reviews."""

    review = graphene.Field(ReviewNode)
    deleted = graphene.Boolean()

    class Input:
        id = graphene.String(required=True)

    @classmethod
    def mutate_and_get_payload(cls, args, context, info):
        try:
            review = get_object(Review, args.get('id'))
            review.delete()
            return cls(deleted=True, review=review)
        except:
            return cls(deleted=False, review=None)
