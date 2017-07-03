import graphene
from graphene_django import DjangoObjectType, DjangoConnectionField
from django_filters import OrderingFilter, FilterSet

from app.timetables.models import Timetable
from .vendor_crud import VendorNode
from .user_crud import UserNode
from .weekday_crud import WeekdayNode


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
            'name': ['icontains']
        }
        model = Timetable


class TimetableNode(DjangoObjectType):
    original_id = graphene.Int()
    vendors = DjangoConnectionField(lambda: VendorNode)
    admins = DjangoConnectionField(lambda: UserNode)
    inactive_weekdays = DjangoConnectionField(lambda: WeekdayNode)

    class Meta:
        model = Timetable
        interfaces = (graphene.relay.Node, )

    def resolve_original_id(self, args, context, info):
        return self.id
