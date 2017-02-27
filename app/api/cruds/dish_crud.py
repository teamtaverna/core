from app.timetables.models import Dish
from django.core.exceptions import ValidationError

import graphene
from graphene_django import DjangoObjectType
from .utils import get_errors, get_object, load_object


class DishNode(DjangoObjectType):
    original_id = graphene.Int()

    class Meta:
        model = Dish
        filter_fields = {
            'name': ['icontains'],
        }
        filter_order_by = ['id', '-id', 'name', '-name', 'date_created',
                           '-date_created', 'date_modified', '-date_modified']
        interfaces = (graphene.relay.Node, )

    def resolve_original_id(self, args, context, info):
        return self.id


class CreateDish(graphene.relay.ClientIDMutation):

    class Input:
        name = graphene.String(required=True)
        description = graphene.String(required=False)

    dish = graphene.Field(DishNode)
    errors = graphene.List(graphene.String)

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        try:
            dish = Dish()
            dish.name = input.get('name')
            dish.description = input.get('description', '')
            dish.full_clean()
            dish.save()
            return CreateDish(dish=dish)
        except ValidationError as e:
            return CreateDish(dish=None, errors=get_errors(e))


class UpdateDish(graphene.relay.ClientIDMutation):

    class Input:
        id = graphene.String(required=True)
        name = graphene.String(required=False)
        description = graphene.String(required=False)

    dish = graphene.Field(DishNode)
    errors = graphene.List(graphene.String)

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        dish = get_object(Dish, input.get('id'))
        dish = load_object(dish, input)
        try:
            if dish:
                dish.full_clean()
                dish.save()
            return UpdateDish(dish=dish)
        except ValidationError as e:
            return UpdateDish(dish=dish, errors=get_errors(e))


class DeleteDish(graphene.relay.ClientIDMutation):

    class Input:
        id = graphene.String(required=True)

    deleted = graphene.Boolean()
    dish = graphene.Field(DishNode)

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        try:
            dish = get_object(Dish, input.get('id'))
            dish.delete()
            return DeleteDish(deleted=True, dish=dish)
        except:
            return DeleteDish(deleted=False, dish=None)
