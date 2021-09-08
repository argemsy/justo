from django.db import models
from django.utils import timezone
from utils.models import BaseModel


class HitManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related("hitmen", "target", "assigned_by")


class Hit(BaseModel):
    code_hit = models.CharField(
        max_length=100,
        verbose_name="Código",
        help_text="varchar(100) *",
        editable=False,
    )
    hitmen = models.ForeignKey(
        "users.User",
        on_delete=models.PROTECT,
        verbose_name="Asesino",
        related_name="hits",
    )
    target = models.ForeignKey(
        "hits.Target",
        verbose_name="Objetivo",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
    )
    status = models.SmallIntegerField(
        choices=(
            (1, "Activo"),
            (2, "Finalizado"),
            (3, "Fallido"),
        ),
        default=1,
        verbose_name="Status del hit",
    )
    level = models.SmallIntegerField(
        choices=(
            (1, "Fácil"),
            (2, "Intermedio"),
            (3, "Difícil"),
        ),
        default=3,
        verbose_name="Level del hit",
    )
    hit_detail = models.TextField(
        blank=True,
        null=True,
        verbose_name="Detalles del hit",
        help_text="text no required",
    )
    status_detail = models.TextField(
        blank=True,
        null=True,
        verbose_name="Detalles del status",
        help_text="text no required",
    )
    assigned_by = models.ForeignKey(
        "users.User",
        on_delete=models.PROTECT,
        verbose_name="Asignado por",
        related_name="assigned_hits",
    )
    objects = HitManager()

    def save(self) -> None:
        if not self.pk:
            date = timezone.now().strftime("%Y%m%d_%H:%M:%S")
            self.code_hit = f"HIT_{str(self.transaction_id).upper()}_{date}"
        return super().save()

    def __str__(self) -> str:
        return f"{self.code_hit}"
