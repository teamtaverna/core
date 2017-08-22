import pytz

from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin

from ipware.ip import get_real_ip
from geolite2 import geolite2


class TimezoneMiddleware(MiddlewareMixin):

    def process_request(self, request):
        user_time_zone = request.session.get('user_time_zone')
        try:
            if not user_time_zone:
                user_ip = get_real_ip(request)
                if user_ip:
                    reader = geolite2.reader()
                    ip_details = reader.get(user_ip)
                    user_time_zone = ip_details['location']['time_zone']
                    geolite2.close()
                    if user_time_zone:
                        request.session['user_time_zone'] = user_time_zone
            timezone.activate(pytz.timezone(user_time_zone))
        except:
            timezone.deactivate()
