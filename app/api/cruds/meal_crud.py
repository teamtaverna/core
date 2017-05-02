"""Set up Graphql for Meal Model"""
import graphene
from graphene_django.types import DjangoObjectType
from graphene_django.converter import convert_django_field

from django.db.models import TimeField
from django.core.exceptions import ValidationError

from app.timetables.models import Meal
from app.api.cruds.utils import get_errors, get_object, load_object


# https://github.com/graphql-python/graphene-django/issues/18
@convert_django_field.register(TimeField)
def convert_function(field, registry=None):
    return graphene.String()


class MealNode(DjangoObjectType):
    """GraphQL Node for Meal model"""

    original_id = graphene.Int()

    class Meta:
        model = Meal
        filter_fields = {
            'name': ['icontains', 'exact']
        }
        # filter_order_by = ['id', 'name', 'start_time', 'end_time']
        interfaces = (graphene.relay.Node, )

    def resolve_original_id(self, args, context, info):
        return self.id


class CreateMeal(graphene.relay.ClientIDMutation):
    """Mutation for creating Meals"""

    class Input:
        name = graphene.String(required=True)
        start_time = graphene.String(required=True)
        end_time = graphene.String(required=True)

    meal = graphene.Field(MealNode)
    errors = graphene.List(graphene.String)

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        try:
            meal = Meal()
            meal.name = input.get('name')
            meal.start_time = input.get('start_time')
            meal.end_time = input.get('end_time')
            meal.full_clean()
            meal.save()
            return cls(meal=meal)
        except ValidationError as e:
            return cls(meal=None, errors=get_errors(e))


class UpdateMeal(graphene.relay.ClientIDMutation):
    """Mutation for creating Meals"""

    class Input:
        id = graphene.String(required=True)
        name = graphene.String(required=False)
        start_time = graphene.String(required=False)
        end_time = graphene.String(required=False)

    meal = graphene.Field(MealNode)
    errors = graphene.List(graphene.String)

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        meal = get_object(Meal, input.get('id'))
        meal = load_object(meal, input)
        try:
            if meal:
                meal.full_clean()
                meal.save()
            return cls(meal=meal)
        except ValidationError as e:
            return cls(meal=meal, errors=get_errors(e))


class DeleteMeal(graphene.relay.ClientIDMutation):
    """Mutation for Deleting Meals"""

    class Input:
        id = graphene.String(required=True)

    deleted = graphene.Boolean()
    meal = graphene.Field(MealNode)

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        try:
            meal = get_object(Meal, input.get('id'))
            meal.delete()
            return cls(deleted=True, meal=meal)
        except:
            return cls(deleted=False, meal=None)
