from django.core.exceptions import ObjectDoesNotExist, ValidationError

import graphene
from graphene_django import DjangoObjectType
from graphql_relay.node.node import from_global_id

from app.timetables.models import Weekday
from .utils import get_errors


class WeekdayNode(DjangoObjectType):
    original_id = graphene.Int()

    class Meta:
        model = Weekday
        filter_fields = {
            'name': ['icontains']
        }
        filter_order_by = ['name', '-name']
        interfaces = (graphene.relay.Node,)

    def resolve_original_id(self, args, context, info):
        return self.id


class CreateWeekday(graphene.relay.ClientIDMutation):
    weekday = graphene.Field(WeekdayNode)
    errors = graphene.List(graphene.String)

    class Input:
        name = graphene.String(required=True)

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        try:
            weekday = Weekday(
                name=input.get('name')
            )
            weekday.full_clean()
            weekday.save()
            return CreateWeekday(weekday=weekday)
        except ValidationError as e:
            return CreateWeekday(weekday=None, errors=get_errors(e))


class UpdateWeekday(graphene.relay.ClientIDMutation):
    weekday = graphene.Field(WeekdayNode)
    errors = graphene.List(graphene.String)

    class Input:
        id = graphene.String(required=True)
        name = graphene.String(required=True)

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        weekday = Weekday.objects.get(pk=from_global_id(input.get('id'))[1])
        weekday.name = input.get('name')
        try:
            weekday.full_clean()
            weekday.save()
            return UpdateWeekday(weekday=weekday)
        except ValidationError as e:
            return UpdateWeekday(weekday=weekday, errors=get_errors(e))


class DeleteWeekday(graphene.relay.ClientIDMutation):
    weekday = graphene.Field(WeekdayNode)
    deleted = graphene.Boolean()

    class Input:
        id = graphene.String(required=True)

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        try:
            weekday = Weekday.objects.get(
                pk=from_global_id(input.get('id'))[1]
            )
            weekday.delete()
            return DeleteWeekday(deleted=True, weekday=weekday)
        except ObjectDoesNotExist:
            return DeleteWeekday(deleted=False, weekday=None)
