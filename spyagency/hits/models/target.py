from django.db import models

from utils.models import BaseModel


class Target(BaseModel):
    first_name = models.CharField(
        max_length=60, verbose_name="Nombre", help_text="varchar(60) required*"
    )
    last_name = models.CharField(
        max_length=60, verbose_name="Apellido", help_text="varchar(60) required*"
    )
    created_by = models.ForeignKey(
        "users.User",
        on_delete=models.PROTECT,
        verbose_name="Creado por",
        related_name="targets",
    )
    extra_info = models.JSONField(
        verbose_name="Información adicional",
        help_text="json no required",
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"{self.first_name}, {self.last_name}"
