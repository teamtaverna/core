from django.conf.urls import url, include
from django.contrib import admin

from graphene_django.views import GraphQLView


urlpatterns = [
    url(r'^api/', include('app.api.urls')),
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^api', GraphQLView.as_view(graphiql=True)),
]
