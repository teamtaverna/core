import pytz
import requests

from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin


class TimezoneMiddleware(MiddlewareMixin):

    def process_request(self, request):
        user_time_zone = request.session.get('user_time_zone')
        try:
            if not user_time_zone:
                freegeoip_response = requests.get('http://freegeoip.net/json')
                user_time_zone = freegeoip_response.json()['time_zone']
                if user_time_zone:
                    request.session['user_time_zone'] = user_time_zone
            timezone.activate(pytz.timezone(user_time_zone))
        except:
            timezone.deactivate()
