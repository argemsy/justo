from django.contrib import admin

from hits.models import Hit
from utils.admin import BaseAdmin


@admin.register(Hit)
class HitAdmin(BaseAdmin):
    list_display = ("id", "code_hit", "hitmen", "target", "assigned_by")
