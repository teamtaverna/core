from django.core.exceptions import ValidationError

import graphene
from graphene_django import DjangoObjectType

from app.timetables.models import Weekday
from .utils import get_errors, get_object, load_object


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
            return cls(weekday=weekday)
        except ValidationError as e:
            return cls(weekday=None, errors=get_errors(e))


class UpdateWeekday(graphene.relay.ClientIDMutation):
    weekday = graphene.Field(WeekdayNode)
    errors = graphene.List(graphene.String)

    class Input:
        id = graphene.String(required=True)
        name = graphene.String(required=True)

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        weekday = get_object(Weekday, input.get('id'))
        weekday = load_object(weekday, input)
        try:
            if weekday:
                weekday.full_clean()
                weekday.save()
            return cls(weekday=weekday)
        except ValidationError as e:
            return cls(weekday=weekday, errors=get_errors(e))


class DeleteWeekday(graphene.relay.ClientIDMutation):
    weekday = graphene.Field(WeekdayNode)
    deleted = graphene.Boolean()

    class Input:
        id = graphene.String(required=True)

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        try:
            weekday = get_object(Weekday, input.get('id'))
            weekday.delete()
            return cls(deleted=True, weekday=weekday)
        except:
            return cls(deleted=False, weekday=None)
