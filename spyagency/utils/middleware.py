from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from rest_framework_jwt.settings import api_settings
from users.models import User

decode_handler = api_settings.JWT_DECODE_HANDLER


class BLKSoftMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_view(self, request, view_func, view_args, view_kwargs):
        jwt = settings.NAME_JWT
        header_cookie = request.COOKIES.get(jwt, None)
        if header_cookie:
            try:
                token = decode_handler(header_cookie)
                user = User.objects.get(username=token["username"])
            except User.DoesNotExist:
                request.user = AnonymousUser
            else:
                request.user = user
