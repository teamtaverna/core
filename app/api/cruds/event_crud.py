import graphene
from graphene_django import DjangoObjectType
from django_filters import OrderingFilter, FilterSet

from app.timetables.models import Event
from .timetable_crud import TimetableNode


class EventNode(DjangoObjectType):
    original_id = graphene.Int()


    class Meta:
        model = Event
        interfaces = (graphene.relay.Node, )

    def resolve_original_id(self, args, context, info):
        return self.id

class EventFilter(FilterSet):
    order_by = OrderingFilter(fields=[('name', 'name'),
                                      ('timetable', 'timetable'),
                                      ('action', 'action'),
                                      ('start_date', 'start_date'),
                                      ('end_date', 'end_date')])
    
    class Meta:
        fields = {
            'name': ['icontains']
        }
        model = Event


class EventNode(DjangoObjectType):
    original_id = graphene.Int()
    timetable = DjangoConnectionField(lambda: TimetableNode)

    class Meta:
        model = Event
        interfaces = (graphene.relay.Node, )
    
    def resolve_original_id(self, args, context, info):
        return self.id
