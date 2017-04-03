import graphene
from graphene_django.filter import DjangoFilterConnectionField

from .cruds.user_crud import UserNode, CreateUser, UpdateUser, DeleteUser
from .cruds.dish_crud import DishNode, CreateDish, UpdateDish, DeleteDish
from .cruds.weekday_crud import (WeekdayNode, CreateWeekday, UpdateWeekday,
                                 DeleteWeekday,)
from .cruds.meal_crud import MealNode, CreateMeal, UpdateMeal


class Query(graphene.AbstractType):
    user = graphene.relay.Node.Field(UserNode)
    users = DjangoFilterConnectionField(UserNode)

    weekday = graphene.relay.Node.Field(WeekdayNode)
    weekdays = DjangoFilterConnectionField(WeekdayNode)

    dish = graphene.relay.Node.Field(DishNode)
    dishes = DjangoFilterConnectionField(DishNode)

    meal = graphene.relay.Node.Field(MealNode)
    meals = DjangoFilterConnectionField(MealNode)

class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()
    delete_user = DeleteUser.Field()

    create_dish = CreateDish.Field()
    update_dish = UpdateDish.Field()
    delete_dish = DeleteDish.Field()

    create_weekday = CreateWeekday.Field()
    update_weekday = UpdateWeekday.Field()
    delete_weekday = DeleteWeekday.Field()

    create_meal = CreateMeal.Field()
    update_meal = UpdateMeal.Field()
