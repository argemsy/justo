from rest_framework.permissions import BasePermission

TOKEN = "mfGQ1qqw6MWjOGJy7hWy18qzD-Z2O7kWDpOVBncNnAo"


class SpyAgentPermission(BasePermission):
    def has_permission(self, request, view):
        token = request.META.get("HTTP_AUTHORIZATION", None)
        if token:
            return token == TOKEN
        return False
