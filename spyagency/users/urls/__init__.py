from django.urls import include, path, re_path

from users.urls.api import router as user_router

app_name = "users"

urlpatterns = [
    re_path(r"^users/api/(?P<version>[-\w]+)/", include(user_router.urls)),
    path("", include("users.urls.views", namespace="views")),
    path("", include("users.urls.account", namespace="account")),
]
