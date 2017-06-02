from app.timetables.models import Dish
from django.core.exceptions import ValidationError

import graphene
from graphene_django import DjangoObjectType
from django_filters import OrderingFilter, FilterSet

from .utils import get_errors, get_object, load_object


class DishFilter(FilterSet):

    order_by = OrderingFilter(fields=[('id', 'id'),
                                      ('name', 'name'),
                                      ('date_created', 'date_created'),
                                      ('date_modified', 'date_modified')]
                              )

    class Meta:
        fields = {'name': ['icontains']}
        model = Dish


class DishNode(DjangoObjectType):
    original_id = graphene.Int()

    class Meta:
        model = Dish
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
    def mutate_and_get_payload(cls, args, context, info):
        try:
            dish = Dish()
            dish.name = args.get('name')
            dish.description = args.get('description', '')
            dish.full_clean()
            dish.save()
            return cls(dish=dish)
        except ValidationError as e:
            return cls(dish=None, errors=get_errors(e))


class UpdateDish(graphene.relay.ClientIDMutation):

    class Input:
        id = graphene.String(required=True)
        name = graphene.String(required=False)
        description = graphene.String(required=False)

    dish = graphene.Field(DishNode)
    errors = graphene.List(graphene.String)

    @classmethod
    def mutate_and_get_payload(cls, args, context, info):
        dish = get_object(Dish, args.get('id'))
        dish = load_object(dish, args)
        try:
            if dish:
                dish.full_clean()
                dish.save()
            return cls(dish=dish)
        except ValidationError as e:
            return cls(dish=dish, errors=get_errors(e))


class DeleteDish(graphene.relay.ClientIDMutation):

    class Input:
        id = graphene.String(required=True)

    deleted = graphene.Boolean()
    dish = graphene.Field(DishNode)

    @classmethod
    def mutate_and_get_payload(cls, args, context, info):
        try:
            dish = get_object(Dish, args.get('id'))
            dish.delete()
            return cls(deleted=True, dish=dish)
        except:
            return cls(deleted=False, dish=None)
