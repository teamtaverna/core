import graphene
from graphene import relay, Field, String, Int, Boolean, List
from graphene_django import DjangoConnectionField, DjangoObjectType
from graphql_relay.node.node import from_global_id
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


def getErrors(e):
    # transform django errors to redux errors
    # django: {"key1": [value1], {"key2": [value2]}}
    # redux: ["key1", "value1", "key2", "value2"]
    fields = e.message_dict.keys()
    messages = ['; '.join(m) for m in e.message_dict.values()]
    errors = [i for pair in zip(fields, messages) for i in pair]
    return errors


class UserNode(DjangoObjectType):
    original_id = Int()

    class Meta:
        model = User
        filter_fields = {
            'username': ['icontains'],
            'is_staff': ['exact'],
            'is_active': ['exact']
        }
        filter_order_by = ['id', '-id', 'username', '-username', 'is_staff',
                           '-is_staff', 'is_active', '-is_active' 'date_joined', '-date_joined']
        interfaces = (relay.Node, )

    def resolve_original_id(self, args, context, info):
        return self.id


def get_user(relayId, otherwise=None):
    try:
        return User.objects.get(pk=from_global_id(relayId)[1])
    except:
        return otherwise


class CreateUser(relay.ClientIDMutation):

    class Input:
        username = String(required=True)
        first_name = String(required=False)
        last_name = String(required=False)
        email = String(required=False)
        is_staff = Boolean(required=False)
        is_active = Boolean(required=False)
        password = String(required=True)

    user = Field(UserNode)
    errors = List(String)

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
            return CreateUser(user=user)
        except ValidationError as e:
            return CreateUser(user=None, errors=getErrors(e))


class UpdateUser(relay.ClientIDMutation):

    class Input:
        id = String(required=True)
        username = String(required=False)
        first_name = String(required=False)
        last_name = String(required=False)
        email = String(required=False)
        is_staff = Boolean(required=False)
        is_active = Boolean(required=False)
        password = String(required=False)

    user = Field(UserNode)
    errors = List(String)

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        user = get_user(input.get('id'))
        for key, value in input.items():
            if key == 'password':
                user.set_password(input.get('password'))
            elif key != 'id':
                setattr(user, key, value)
        try:
            user.full_clean()
            user.save()
            return UpdateUser(user=user)
        except ValidationError as e:
            return UpdateUser(user=user, errors=getErrors(e))


class DeleteUser(relay.ClientIDMutation):

    class Input:
        id = String(required=True)

    deleted = Boolean()
    user = Field(UserNode)

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        try:
            user = get_user(input.get('id'))
            user.delete()
            return DeleteUser(deleted=True, user=user)
        except:
            return DeleteUser(deleted=False, user=None)


class Query(graphene.AbstractType):
    user = relay.Node.Field(UserNode)
    users = DjangoConnectionField(UserNode)


class UserMutations(graphene.ObjectType):
    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()
    delete_user = DeleteUser.Field()
