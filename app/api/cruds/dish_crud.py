from app.timetables.models import Dish

import graphene
from graphene_django import DjangoObjectType


class DishNode(DjangoObjectType):
    original_id = graphene.Int()

    class Meta:
        model = Dish
        filter_fields = {
            'name': ['icontains'],
        }
        filter_order_by = ['id', '-id', 'name', '-name', 'date_created', '-date_created']
        interfaces = (graphene.relay.Node, )

    def resolve_original_id(self, args, context, info):
        return self.id