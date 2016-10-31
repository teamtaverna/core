import graphene

from app.api import schema as api_schema


class Query(api_schema.Query, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query)
