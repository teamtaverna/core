from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

import graphene
from graphene_django import DjangoObjectType

from .utils import get_errors, get_object, load_object
from app.accounts.models import UserProfile
from .inputs import ProfileInput, UserCreateInput


class ProfileNode(DjangoObjectType):
    original_id = graphene.Int()

    class Meta:
        model = UserProfile
        interfaces = (graphene.relay.Node, )

    def resolve_original_id(self, args, context, info):
        return self.id


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
        user = graphene.Argument(UserCreateInput)
        profile = graphene.Argument(ProfileInput)

    user = graphene.Field(UserNode)
    errors = graphene.List(graphene.String)

    @classmethod
    def mutate_and_get_payload(cls, args, context, info):
        try:
            user = User()
            user_data = args.get('user')
            user.username = user_data.get('username')
            user.first_name = user_data.get('first_name', '')
            user.last_name = user_data.get('last_name', '')
            user.email = user_data.get('email', '')
            user.is_staff = user_data.get('is_staff', False)
            user.is_active = user_data.get('is_active', False)
            if user_data.get('password'):
                user.set_password(user_data.get('password'))
            user.full_clean()
            user.save()
            profile_data = args.get('profile')
            if profile_data:
                profile = load_object(user.profile, profile_data)
                if profile:
                    profile.save()

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
        profile = graphene.Argument(ProfileInput)

    user = graphene.Field(UserNode)
    errors = graphene.List(graphene.String)

    @classmethod
    def mutate_and_get_payload(cls, args, context, info):
        user = get_object(User, args.get('id'))
        user = load_object(user, args, ['id', 'password', 'profile'])

        if user:
            if 'password' in args:
                user.set_password(args['password'])

            try:
                user.full_clean()
                user.save()
                profile_data = args.get('profile')
                if profile_data:
                    profile = user.profile if isinstance(user.profile, UserProfile) \
                        else UserProfile()
                    profile = load_object(profile, profile_data)
                    if profile:
                        profile.save()
            except ValidationError as e:
                return cls(user=user, errors=get_errors(e))

        return cls(user=user)


class DeleteUser(graphene.relay.ClientIDMutation):

    class Input:
        id = graphene.String(required=True)

    deleted = graphene.Boolean()
    user = graphene.Field(UserNode)

    @classmethod
    def mutate_and_get_payload(cls, args, context, info):
        try:
            user = get_object(User, args.get('id'))
            user.delete()
            return cls(deleted=True, user=user)
        except:
            return cls(deleted=False, user=None)
