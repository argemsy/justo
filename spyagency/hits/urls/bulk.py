from django.urls import path

from utils.jwt_mixin import JWTView

app_name = "bulk"

urlpatterns = [
    path("", JWTView.as_view(template_name="hits/bulk.html"), name="list"),
]
