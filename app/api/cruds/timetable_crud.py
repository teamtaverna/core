from django.core.exceptions import ValidationError

import graphene
from graphene_django import DjangoObjectType, DjangoConnectionField
from django_filters import OrderingFilter, FilterSet

from app.timetables.models import Timetable, VendorService, TimetableManagement
from .utils import get_errors, get_object, load_object
from .vendor_crud import VendorNode
from .user_crud import UserNode


class TimetableFilter(FilterSet):

    order_by = OrderingFilter(fields=[('id', 'id'),
                                      ('name', 'name'),
                                      ('cycle_length', 'cycle_length'),
                                      ('ref_cycle_length', 'ref_cycle_length'),
                                      ('ref_cycle_date', 'ref_cycle_date'),
                                      ('inactive_weekdays', 'inactive_weekdays'),
                                      ('is_active', 'is_active'),
                                      ('date_created', 'date_created'),
                                      ('date_modified', 'date_modified')]
                              )

    class Meta:
        fields = {
            'name': ['icontains'],
            'code': ['exact']
        }
        model = Timetable


class TimetableNode(DjangoObjectType):
    original_id = graphene.Int()
    vendors = DjangoConnectionField(lambda: VendorNode)
    users = DjangoConnectionField(lambda: UserNode)

    class Meta:
        model = Timetable
        interfaces = (graphene.relay.Node, )

    def resolve_original_id(self, args, context, info):
        return self.id


class CreateTimetable(graphene.relay.ClientIDMutation):

    class Input:
        name = graphene.String(required=True)
        code = graphene.String(required=True)
        cycle_length = graphene.Int(required=True)
        ref_cycle_day = graphene.Int(required=True)
        ref_cycle_date = graphene.String(required=True)
        inactive_weekdays = graphene.Int(required=False)
        vendor_id = graphene.Int(required=False)
        is_active = graphene.Boolean(required=False)
        description = graphene.String(required=False)
        admin_id = graphene.Int(required=False)

    timetable = graphene.Field(TimetableNode)
    errors = graphene.List(graphene.String)

    @classmethod
    def mutate_and_get_payload(cls, args, context, info):
        try:
            timetable = Timetable()
            timetable.name = args.get('name')
            timetable.code = args.get('code')
            timetable.cycle_length = args.get('cycle_length')
            timetable.ref_cycle_day = args.get('ref_cycle_day')
            timetable.ref_cycle_date = args.get('ref_cycle_date')
            timetable.is_active = args.get('is_active', True)
            timetable.description = args.get('description', '')
            timetable.full_clean()
            timetable.save()
            ### TO FIX:
            ### This part is buggy. Try to save vendor, admin and weekday appropriately
            vendor = VendorService.objects.get(id=args.get('vendor_id'))
            if vendor:
                timetable.vendorservice_set.add(vendor)

            admin = TimetableManagement.objects.get(id=args.get('admin_id'))
            if admin:
                timetable.timetablemanagement_set.add(admin)
            # Add implementation for weekday also
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
