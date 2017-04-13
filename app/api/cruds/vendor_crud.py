import graphene
from graphene_django import DjangoObjectType

from app.timetables.models import Vendor


class VendorNode(DjangoObjectType):
    original_id = graphene.Int()

    class Meta:
        model = Vendor
        filter_fields = {
            'name': ['icontains']
        }
        filter_order_by = ['name', '-name']
        interfaces = (graphene.relay.Node,)

    def resolve_original_id(self, args, context, info):
        return self.id
