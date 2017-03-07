from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist

import graphene
from graphene_django import DjangoObjectType

from .utils import get_object, get_errors


class UserNode(DjangoObjectType):
    original_id = graphene.Int()

    class Meta:
        model = User
        filter_fields = {
            'username': ['icontains'],
            'is_staff': ['exact'],
            'is_active': ['exact']
        }
        filter_order_by = ['id', '-id', 'username', '-username', 'is_staff',
                           '-is_staff', 'is_active', '-is_active', 'date_joined', '-date_joined']
        interfaces = (graphene.relay.Node, )

    def resolve_original_id(self, args, context, info):
        return self.id


class CreateUser(graphene.relay.ClientIDMutation):

    class Input:
        username = graphene.String(required=True)
        first_name = graphene.String(required=False)
        last_name = graphene.String(required=False)
        email = graphene.String(required=False)
        is_staff = graphene.Boolean(required=False)
        is_active = graphene.Boolean(required=False)
        password = graphene.String(required=True)

    user = graphene.Field(UserNode)
    errors = graphene.List(graphene.String)

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        try:
            user = User()
            user.username = input.get('username')
            user.first_name = input.get('first_name', '')
            user.last_name = input.get('last_name', '')
            user.email = input.get('email', '')
            user.is_staff = input.get('is_staff', False)
            user.is_active = input.get('is_active', False)
            if input.get('password'):
                user.set_password(input.get('password'))
            user.full_clean()
            user.save()
            return cls(user=user)
        except ValidationError as e:
            return cls(user=None, errors=get_errors(e))


class UpdateUser(graphene.relay.ClientIDMutation):

    class Input:
        id = graphene.String(required=True)
        username = graphene.String(required=False)
        first_name = graphene.String(required=False)
        last_name = graphene.String(required=False)
        email = graphene.String(required=False)
        is_staff = graphene.Boolean(required=False)
        is_active = graphene.Boolean(required=False)
        password = graphene.String(required=False)

    user = graphene.Field(UserNode)
    errors = graphene.List(graphene.String)

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        user = get_object(User, input.get('id'))
        for key, value in input.items():
            if key == 'password':
                user.set_password(input.get('password'))
            elif key != 'id':
                setattr(user, key, value)
        try:
            user.full_clean()
            user.save()
            return cls(user=user)
        except ValidationError as e:
            return cls(user=user, errors=get_errors(e))


class DeleteUser(graphene.relay.ClientIDMutation):

    class Input:
        id = graphene.String(required=True)

    deleted = graphene.Boolean()
    user = graphene.Field(UserNode)

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        try:
            user = get_object(User, input.get('id'))
            user.delete()
            return cls(deleted=True, user=user)
        except ObjectDoesNotExist:
            return cls(deleted=False, user=None)
