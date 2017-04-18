from django.core.exceptions import ValidationError

import graphene
from graphene_django import DjangoObjectType

from app.timetables.models import Vendor
from .utils import get_errors, get_object, load_object


class VendorNode(DjangoObjectType):
    """API functionality for vendor model. """

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


class CreateVendor(graphene.relay.ClientIDMutation):
    """API functionality to create vendors."""

    vendor = graphene.Field(VendorNode)
    errors = graphene.List(graphene.String)

    class Input:
        name = graphene.String(required=True)
        info = graphene.String(required=False)

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        try:
            vendor = Vendor(
                name=input.get('name'),
                info=input.get('info', '')
            )
            vendor.full_clean()
            vendor.save()
            return cls(vendor=vendor)
        except ValidationError as e:
            return cls(vendor=None, errors=get_errors(e))


class UpdateVendor(graphene.relay.ClientIDMutation):
    """API functionality to update vendors."""

    vendor = graphene.Field(VendorNode)
    errors = graphene.List(graphene.String)

    class Input:
        id = graphene.String(required=True)
        name = graphene.String(required=True)
        info = graphene.String(required=False)

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        vendor = get_object(Vendor, input.get('id'))
        vendor = load_object(vendor, input)
        try:
            if vendor:
                vendor.full_clean()
                vendor.save()
            return cls(vendor=vendor)
        except ValidationError as e:
            return cls(vendor=vendor, errors=get_errors(e))
