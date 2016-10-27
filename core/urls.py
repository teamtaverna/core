from django.conf.urls import url
from django.contrib import admin

from graphene_django.views import GraphQLView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api', GraphQLView.as_view()),
]
