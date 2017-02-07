from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt

from .views import ApiKeyView

urlpatterns = [
    url(r'^api_key$', csrf_exempt(ApiKeyView.as_view())),
    url(r'^api_key/(?P<token>[0-9a-f]*)$', csrf_exempt(ApiKeyView.as_view())),
]
