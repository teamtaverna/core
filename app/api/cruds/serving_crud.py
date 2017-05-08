import graphene
from graphene_django import DjangoObjectType
from graphene_django.converter import convert_django_field
from hashid_field import HashidField

from app.timetables.models import Course, MenuItem, Serving


@convert_django_field.register(HashidField)
def hashidfield_convert(field, registry=None):
    return graphene.String()


class ServingNode(DjangoObjectType):
    original_id = graphene.Int()

    class Meta:
        model = Serving
        interfaces = (graphene.relay.Node, )

    def resolve_original_id(self, args, context, info):
        return self.id


class MenuItemNode(DjangoObjectType):
    original_id = graphene.Int()

    class Meta:
        model = MenuItem
        interfaces = (graphene.relay.Node, )

    def resolve_original_id(self, args, context, info):
        return self.id


class CourseNode(DjangoObjectType):
    original_id = graphene.Int()

    class Meta:
        model = Course
        interfaces = (graphene.relay.Node, )

    def resolve_original_id(self, args, context, info):
        return self.id
