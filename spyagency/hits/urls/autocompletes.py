from django.urls import path

from hits.autocompletes import HitmenAutocomplete

app_name = "autocompletes"

urlpatterns = [
    path("hitmens/", HitmenAutocomplete.as_view(), name="hitmen"),
]
