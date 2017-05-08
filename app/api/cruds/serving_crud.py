from django.db.models.fields import TimeField

import graphene
from graphene_django import DjangoObjectType
from graphene_django.converter import convert_django_field
from hashid_field import HashidField

from app.timetables.models import Course, Meal, MenuItem, Serving, Timetable, Vendor


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


class TimetableNode(DjangoObjectType):
    original_id = graphene.Int()

    class Meta:
        model = Timetable
        exclude_fields = ['admins', 'inactive_weekdays', 'vendors']
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
