from django.urls import path

from utils.jwt_mixin import JWTView

app_name = "views"

urlpatterns = [
    path("", JWTView.as_view(template_name="hits/list.html"), name="list"),
    path("create/", JWTView.as_view(template_name="hits/create.html"), name="create"),
    path("<int:pk>/", JWTView.as_view(template_name="hits/detail.html"), name="detail"),
]
