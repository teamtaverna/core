from django.conf.urls import url, include
from django.contrib import admin
from django.views.decorators.csrf import csrf_exempt

from graphene_django.views import GraphQLView

from app.api.auth import authorization_required

urlpatterns = [
    url(r'^api/', include('app.api.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^api$', csrf_exempt(authorization_required(GraphQLView.as_view()))),
    url(r'^gh$', csrf_exempt(GraphQLView.as_view(graphiql=True))),
]
