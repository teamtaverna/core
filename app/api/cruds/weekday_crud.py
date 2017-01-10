from django.core.exceptions import ValidationError

import graphene
from graphene_django import DjangoObjectType

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

    class Input:
        name = graphene.String(required=True)

    weekday = graphene.Field(WeekdayNode)
    errors = graphene.List(graphene.String)

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        try:
            weekday = Weekday()
            weekday.name = input.get('name')
            weekday.full_clean()
            weekday.save()
            return Weekday(weekday=weekday)
        except ValidationError as e:
            return Weekday(weekday=None, errors=get_errors(e))
