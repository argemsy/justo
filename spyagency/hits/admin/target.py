from django.contrib import admin

from hits.models import Target
from utils.admin import BaseAdmin


@admin.register(Target)
class TargetAdmin(BaseAdmin):
    list_display = ("id", "first_name", "last_name")
