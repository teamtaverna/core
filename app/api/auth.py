from django.http import JsonResponse

from .models import ApiKey


def authorization_required(func=None):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            api_key = 'HTTP_X_TAVERNATOKEN'
            if api_key not in request.META:
                data = {'message': 'Set your api_key in X-TavernaToken header.'}
                return JsonResponse(data, status=401)

            try:
                ApiKey.objects.get(token=request.META[api_key], revoked=False)
            except (ApiKey.DoesNotExist, TypeError):
                data = {'message': 'Invalid Token.'}
                return JsonResponse(data, status=401)

            return view_func(request, *args, **kwargs)

        return wrapper

    if func:
        return decorator(func)

    return decorator
