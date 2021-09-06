import json

from django.conf import settings
from django.http import HttpResponse
from django.urls import reverse
from django.utils import timezone


def javascript_vars(request):
    date = timezone.now()

    context = {
        "date": date.strftime("%d-%m-%Y"),
        "token_drf": "mfGQ1qqw6MWjOGJy7hWy18qzD-Z2O7kWDpOVBncNnAo",
        "name_jwt": settings.NAME_JWT,
        "next": settings.LOGIN_REDIRECT_URL,
        # === api de usuario === #
        "api_user": reverse("users:user-profile", kwargs={"version": "v1"}),
        # === api de usuario === #
    }

    let = "let Django = " + json.dumps(context, indent=1)
    return HttpResponse(let, content_type="application/javascript")
