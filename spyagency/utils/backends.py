from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from rest_framework_jwt.settings import api_settings

jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
User = get_user_model()


class EmailAuthBackend(ModelBackend):
    """Allow users to log in with their email address"""

    def authenticate(self, request, username=None, password=None, **kwargs):
        # Some authenticators expect to authenticate by 'username'
        email = username
        if email is None:
            email = kwargs.get("username")

        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                user.backend = "%s.%s" % (self.__module__, self.__class__.__name__)
                return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
