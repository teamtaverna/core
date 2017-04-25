from django.core.exceptions import ValidationError

import graphene
from graphene_django import DjangoObjectType

from app.timetables.models import Timetable
from .utils import get_errors, get_object, load_object


class TimetableNode(DjangoObjectType):
    original_id = graphene.Int()

    class Meta:
        model = Timetable
        filter_fields = {
            'name': ['icontains'],
            'code': ['exact']
        }
        filter_order_by = ['id', '-id', 'name', '-name', 'cycle_length',
                           '-cycle_length', 'ref_cycle_length', '-ref_cycle_length',
                           'ref_cycle_date', '-ref_cycle_date', 'inactive_weekdays',
                           '-inactive_weekdays', 'vendors', '-vendors', 'is_active',
                           '-is_active', 'admins', '-admins', 'date_created',
                           '-date_created', 'date_modified', '-date_modified']
        interfaces = (graphene.relay.Node, )

    def resolve_original_id(self, args, context, info):
        return self.id


class CreateTimetable(graphene.relay.ClientIDMutation):

    class Input:
        name = graphene.String(required=True)
        cycle_length = graphene.Int(required=True)
        ref_cycle_day = graphene.Int(required=True)
        ref_cycle_date = graphene.Int(required=True)
        inactive_weekdays = graphene.String(required=False)
        vendors = graphene.String(required=True)
        is_active = graphene.Boolean(required=False)
        description = graphene.String(required=False)
        admin = graphene.String(required=True)

    timetable = graphene.Field(TimetableNode)
    errors = graphene.List(graphene.String)

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        try:
            timetable = Timetable()
            timetable.name = input.get('name')
            timetable.cycle_length = input.get('cycle_length')
            timetable.ref_cycle_day = input.get('ref_cycle_day')
            timetable.ref_cycle_date = input.get('ref_cycle_date')
            timetable.inactive_weekdays = input.get('inactive_weekdays', '')
            timetable.vendors = input.get('vendors')
            timetable.is_active = input.get('is_active', True)
            timetable.description = input.get('description', '')
            timetable.admin = input.get('admin')
            timetable.full_clean()
            timetable.save()
            return cls(timetable=timetable)
        except ValidationError as e:
            return cls(timetable=None, errors=get_errors(e))


class UpdateTimetable(graphene.relay.ClientIDMutation):

    class Input:
        id = graphene.String(required=True)
        name = graphene.String(required=False)
        cycle_length = graphene.Int(required=False)
        ref_cycle_day = graphene.Int(required=False)
        ref_cycle_date = graphene.Int(required=False)
        inactive_weekdays = graphene.String(required=False)
        vendors = graphene.String(required=False)
        is_active = graphene.Boolean(required=False)
        description = graphene.String(required=False)
        admin = graphene.String(required=False)

    timetable = graphene.Field(TimetableNode)
    errors = graphene.List(graphene.String)

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        timetable = get_object(Timetable, input.get('id'))
        timetable = load_object(timetable, input)
        try:
            if timetable:
                timetable.full_clean()
                timetable.save()
            return cls(timetable=timetable)
        except ValidationError as e:
            return cls(timetable=timetable, errors=get_errors(e))


class DeleteTimetable(graphene.relay.ClientIDMutation):

    class Input:
        id = graphene.String(required=True)

    deleted = graphene.Boolean()
    timetable = graphene.Field(TimetableNode)

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        try:
            timetable = get_object(Timetable, input.get('id'))
            timetable.delete()
            return cls(deleted=True, timetable=timetable)
        except:
            return cls(deleted=False, timetable=None)
