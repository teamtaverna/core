import graphene
from graphene_django.filter import DjangoFilterConnectionField

from .cruds.user_crud import UserNode, CreateUser, UpdateUser, DeleteUser
from .cruds.dish_crud import DishNode, CreateDish, UpdateDish, DeleteDish


class Query(graphene.AbstractType):
    user = graphene.relay.Node.Field(UserNode)
    users = DjangoFilterConnectionField(UserNode)

    dish = graphene.relay.Node.Field(DishNode)
    dishes = DjangoFilterConnectionField(DishNode)


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()
    delete_user = DeleteUser.Field()

    create_dish = CreateDish.Field()
    update_dish = UpdateDish.Field()
    delete_dish = DeleteDish.Field()
