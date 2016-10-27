import graphene

import app.api.schema


class Query(app.api.schema.Query, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query)
