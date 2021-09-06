from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.views.static import serve

from utils.javascript import javascript_vars

urlpatterns = [
    path("admin/", admin.site.urls),
    path("javascript", javascript_vars, name="javascript"),
    path("", include("users.urls", namespace="users")),
    path("", include("hits.urls", namespace="hits")),
    path(
        "media/<path:path>",
        serve,
        {
            "document_root": settings.MEDIA_ROOT,
        },
    ),
    path(
        "static/<path:path>",
        serve,
        {
            "document_root": settings.STATIC_ROOT,
        },
    ),
]
