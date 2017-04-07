import graphene


class ProfileInput(graphene.InputObjectType):
    custom_auth_id = graphene.String(required=False)
    facebook_oauth_id = graphene.String(required=False)
    google_oauth_id = graphene.String(required=False)
    twitter_oauth_id = graphene.String(required=False)
