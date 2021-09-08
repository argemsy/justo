from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME, authenticate, get_user_model
from django.contrib.auth.mixins import AccessMixin
from django.contrib.auth.views import redirect_to_login
from django.shortcuts import resolve_url
from django.views.generic import TemplateView
from rest_framework_jwt.settings import api_settings
from six.moves.urllib.parse import urlparse

jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
User = get_user_model()


def redirect(request):
    path = request.build_absolute_uri()
    resolved_login_url = resolve_url(settings.LOGIN_URL)
    # If the login url is the same scheme and net location then just
    # use the path as the "next" url.
    login_scheme, login_netloc = urlparse(resolved_login_url)[:2]
    current_scheme, current_netloc = urlparse(path)[:2]
    if (not login_scheme or login_scheme == current_scheme) and (not login_netloc or login_netloc == current_netloc):
        path = request.get_full_path()

    return redirect_to_login(path, resolved_login_url, REDIRECT_FIELD_NAME)


class JWTMixin(AccessMixin):

    jwt = settings.NAME_JWT

    def validate(self, request):
        if self.jwt in request.COOKIES:
            try:
                jwt = request.COOKIES[self.jwt]
                decode = jwt_decode_handler(jwt)
                User.objects.get(username=decode["username"])
                return True
            except Exception as e:
                print(e)
                return False

        return False

    def dispatch(self, request, *args, **kwargs):
        if not self.validate(request):
            response = redirect(request)
            if self.jwt in request.COOKIES:
                del request.COOKIES[self.jwt]
                response.delete_cookie(self.jwt)
            return response
        elif not request.COOKIES[self.jwt]:
            response = redirect(request)
            return response
        return super().dispatch(request, *args, **kwargs)


class JWTView(JWTMixin, TemplateView):
    pass
