import graphene


class ProfileInput(graphene.InputObjectType):
    custom_auth_id = graphene.String(required=False)
    facebook_oauth_id = graphene.String(required=False)
    google_oauth_id = graphene.String(required=False)
    twitter_oauth_id = graphene.String(required=False)


class UserCreateInput(graphene.InputObjectType):
    username = graphene.String(required=True)
    first_name = graphene.String(required=False)
    last_name = graphene.String(required=False)
    email = graphene.String(required=False)
    is_staff = graphene.Boolean(required=False)
    is_active = graphene.Boolean(required=False)
    password = graphene.String(required=True)


class UserUpdateInput(graphene.InputObjectType):
    username = graphene.String(required=False)
    first_name = graphene.String(required=False)
    last_name = graphene.String(required=False)
    email = graphene.String(required=False)
    is_staff = graphene.Boolean(required=False)
    is_active = graphene.Boolean(required=False)
    password = graphene.String(required=False)
