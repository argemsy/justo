from django.urls import path, re_path
from django.urls.conf import include
from django.views.generic import TemplateView

app_name = "account"

urlpatterns = [
    path("auth/", include("users.urls.jwt", namespace="auth")),
    path("", TemplateView.as_view(template_name="users/login.html"), name="login"),
    path(
        "register",
        TemplateView.as_view(template_name="users/register.html"),
        name="register",
    ),
]
