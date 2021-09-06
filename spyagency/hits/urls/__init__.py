from django.urls import include, path, re_path

from hits.urls.api import router as hits_router

app_name = "hits"

urlpatterns = [
    path("hits/", include("hits.urls.views", namespace="views")),
    path(
        "hits/autocompletes/",
        include("hits.urls.autocompletes", namespace="autocompletes"),
    ),
    re_path(r"^hits/api/(?P<version>[-\w]+)/", include(hits_router.urls)),
    path("bulk/", include("hits.urls.bulk", namespace="bulk")),
]
