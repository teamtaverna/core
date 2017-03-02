"""Set up Graphql for Meal Model"""
import graphene
from graphene_django.types import DjangoObjectType
from graphene_django.converter import convert_django_field

from django.db.models import TimeField

from app.timetables.models import Meal as MealModel

# https://github.com/graphql-python/graphene-django/issues/18
@convert_django_field.register(TimeField)
def convert_function(field, registry=None):
    return graphene.String()

class MealNode(DjangoObjectType):
    """GraphQL Node for Meal model"""
    original_id = graphene.Int()

    class Meta:
        model = MealModel
        filter_fields = {
            'name': ['icontains', 'exact']
        }
        filter_order_by = ['id', 'start_time']
        interfaces = (graphene.relay.Node, )

    def resolve_original_id(self, args, context, info):
        return self.id


class CreateMeal(graphene.relay.ClientIDMutation):
    """Mutation for creating Meals"""

    class Input:
        name = graphene.String(require=True)
        start_time = graphene.String(require=True)
        end_time = graphene.String(require=True)

    meal = graphene.Field(MealNode)
    errors = graphene.List(graphene.String)

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        try:
            meal = MealModel()
            meal.name = input.get('name')
            meal.start_time = input.get('start_time', '')
            meal.end_time = input.get('end_time', '')
            meal.full_clean()
            meal.save()
            return cls(meal=meal)
        except ValidationError as e:
            return cls(meal=None, errors=get_errors(e))


# class UpdateMeal(graphene.relay.ClientIDMutation):
#     """Mutation for creating Meals"""
#     pass


# class DeleteMeal(graphene.relay.ClientIDMutation):
#     """Mutation for creating Meals"""
#     pass
