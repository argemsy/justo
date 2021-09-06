from django.urls import path
from django.urls.conf import include
from django.views.generic import TemplateView

app_name = "views"

urlpatterns = [
    path(
        "hitmen/",
        TemplateView.as_view(template_name="hitmen/list.html"),
        name="hitmen_list",
    ),
]
