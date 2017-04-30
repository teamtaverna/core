import graphene
from graphene_django import DjangoConnectionField

from .cruds.user_crud import UserNode, CreateUser, UpdateUser, DeleteUser
from .cruds.dish_crud import DishNode, CreateDish, UpdateDish, DeleteDish
from .cruds.timetable_crud import (TimetableNode, CreateTimetable,
                                   UpdateTimetable, DeleteTimetable,)
from .cruds.weekday_crud import (WeekdayNode, CreateWeekday, UpdateWeekday,
                                 DeleteWeekday,)
from .cruds.meal_crud import MealNode, CreateMeal, UpdateMeal, DeleteMeal
from .cruds.vendor_crud import (VendorNode, CreateVendor, UpdateVendor,
                                DeleteVendor,)


class Query(graphene.AbstractType):
    user = graphene.relay.Node.Field(UserNode)
    users = DjangoConnectionField(UserNode)

    weekday = graphene.relay.Node.Field(WeekdayNode)
    weekdays = DjangoConnectionField(WeekdayNode)

    dish = graphene.relay.Node.Field(DishNode)
    dishes = DjangoConnectionField(DishNode)

    meal = graphene.relay.Node.Field(MealNode)
    meals = DjangoConnectionField(MealNode)

    vendor = graphene.relay.Node.Field(VendorNode)
    vendors = DjangoConnectionField(VendorNode)

    timetable = graphene.relay.Node.Field(TimetableNode)
    timetables = DjangoConnectionField(TimetableNode)


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()
    delete_user = DeleteUser.Field()

    create_dish = CreateDish.Field()
    update_dish = UpdateDish.Field()
    delete_dish = DeleteDish.Field()

    create_timetable = CreateTimetable.Field()
    update_timetable = UpdateTimetable.Field()
    delete_timetable = DeleteTimetable.Field()

    create_weekday = CreateWeekday.Field()
    update_weekday = UpdateWeekday.Field()
    delete_weekday = DeleteWeekday.Field()

    create_meal = CreateMeal.Field()
    update_meal = UpdateMeal.Field()
    delete_meal = DeleteMeal.Field()

    create_vendor = CreateVendor.Field()
    update_vendor = UpdateVendor.Field()
    delete_vendor = DeleteVendor.Field()
