import graphene
from graphene_django.filter import DjangoFilterConnectionField

from .cruds.user_crud import UserNode, CreateUser, UpdateUser, DeleteUser


class Query(graphene.AbstractType):
    user = graphene.relay.Node.Field(UserNode)
    users = DjangoFilterConnectionField(UserNode)


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()
    delete_user = DeleteUser.Field()
