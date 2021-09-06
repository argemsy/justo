from django.urls import path
from rest_framework_jwt.views import (
    obtain_jwt_token,
    refresh_jwt_token,
    verify_jwt_token,
)

app_name = "auth"

urlpatterns = [
    path("obtain-token/", obtain_jwt_token, name="obtain_token"),
    path("refresh-token/", refresh_jwt_token, name="refresh_token"),
    path("verify-token/", verify_jwt_token, name="verify_token"),
]
