# -*- coding: utf-8

# Librerias Standard
import os
from datetime import datetime

# Librerias Django
from django.contrib.auth.models import AbstractUser, Group
from django.db import models
from django.db.models import ImageField
from django.db.models.expressions import Case, F, Q, Value, When
from django.utils import timezone
from rest_framework import permissions

# Librerias en carpetas locales
from utils.sobre_escribir_avatar import SobreEscribirAvatar


def image_path(instance, filename):
    return os.path.join("avatar", str(instance.pk) + "." + filename.rsplit(".", 1)[1])


class User(AbstractUser):
    GENDER_CHOICES = (
        (1, "FEMENINO"),
        (2, "MASCULINO"),
    )
    gender: int = models.SmallIntegerField(choices=GENDER_CHOICES, default=GENDER_CHOICES[1][0], verbose_name="Género")
    bio: str = models.TextField(blank=True, null=True, verbose_name="Biografía")
    died: bool = models.BooleanField(
        default=False,
        verbose_name="Fallecido",
        help_text="Indica si no ha perdido la vida",
    )
    died_date: datetime = models.DateField(verbose_name="Fecha de muerte", blank=True, null=True)
    retired: bool = models.BooleanField(
        default=False, verbose_name="Retirado", help_text="Indica si no se ha retirado"
    )
    retired_date: datetime = models.DateField(verbose_name="Fecha de retiro", blank=True, null=True)
    avatar: ImageField = models.ImageField(
        max_length=255,
        storage=SobreEscribirAvatar(),
        upload_to=image_path,
        blank=True,
        null=True,
        default="avatar/default_avatar.png",
    )

    class Meta:
        ordering = ["-id"]
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
        db_table = "auth_user"
        permissions = [
            ("big_boss_menu", "Big Boss menu"),
            ("manager_menu", "Manager's menu"),
            ("hitmen_menu", "Hitmen menu"),
        ]

    def __str__(self):
        return f"{self.username}"

    @property
    def get_short_name(self):
        return "%s %s" % (self.first_name, self.last_name)

    @property
    def get_rol_name(self):
        if self.groups.filter(name__iexact="big_boss").exists():
            return "Big Boss"
        elif self.groups.filter(name__iexact="managers").exists():
            return "Manager"
        else:
            return "Killer"

    @property
    def get_team_name(self):
        if self.groups.filter(name__iexact="big_boss").exists():
            return "big_boss"
        elif self.groups.filter(name__iexact="managers").exists():
            return "managers"
        elif self.groups.exclude(id__in=[1, 2]).exists():
            return self.groups.exclude(id__in=[1, 2])[0].name
        else:
            return ""
