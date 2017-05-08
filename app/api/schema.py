import graphene
from graphene_django.filter import DjangoFilterConnectionField

from .cruds.user_crud import (UserNode, CreateUser, UpdateUser, DeleteUser,
                              UserFilter,)
from .cruds.dish_crud import (DishNode, CreateDish, UpdateDish, DeleteDish,
                              DishFilter,)
from .cruds.timetable_crud import TimetableNode, TimetableFilter
from .cruds.weekday_crud import (WeekdayNode, CreateWeekday, UpdateWeekday,
                                 DeleteWeekday, WeekdayFilter)
from .cruds.meal_crud import (MealNode, CreateMeal, UpdateMeal, DeleteMeal,
                              MealFilter,)
from .cruds.vendor_crud import (VendorNode, CreateVendor, UpdateVendor,
                                DeleteVendor, VendorFilter)


class Query(graphene.AbstractType):
    user = graphene.relay.Node.Field(UserNode)
    users = DjangoFilterConnectionField(UserNode, filterset_class=UserFilter)

    weekday = graphene.relay.Node.Field(WeekdayNode)
    weekdays = DjangoFilterConnectionField(WeekdayNode,
                                           filterset_class=WeekdayFilter)

    dish = graphene.relay.Node.Field(DishNode)
    dishes = DjangoFilterConnectionField(DishNode, filterset_class=DishFilter)

    meal = graphene.relay.Node.Field(MealNode)
    meals = DjangoFilterConnectionField(MealNode, filterset_class=MealFilter)

    vendor = graphene.relay.Node.Field(VendorNode)
    vendors = DjangoFilterConnectionField(VendorNode,
                                          filterset_class=VendorFilter)

    timetable = graphene.relay.Node.Field(TimetableNode)
    timetables = DjangoFilterConnectionField(TimetableNode,
                                             filterset_class=TimetableFilter)


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
    delete_meal = DeleteMeal.Field()

    create_vendor = CreateVendor.Field()
    update_vendor = UpdateVendor.Field()
    delete_vendor = DeleteVendor.Field()
