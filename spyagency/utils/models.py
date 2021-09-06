import uuid

from django.db import connection, models
from simple_history.models import HistoricalRecords


class BaseModel(models.Model):
    """
    Modelo Abstracto con historico de respaldo
    """

    transaction_id: str = models.UUIDField(
        db_index=True,
        null=True,
        blank=True,
        editable=False,
        verbose_name="Identificador",
        help_text="UUID",
        default=uuid.uuid4,
    )
    pub_date: str = models.DateTimeField(
        auto_now_add=True,
        editable=True,
        verbose_name="Fecha de Creación",
        help_text="DateTime",
    )
    mod_date: str = models.DateTimeField(
        auto_now=True, verbose_name="Fecha de modificación", help_text="DateTime"
    )
    is_active: bool = models.BooleanField(
        default=True, verbose_name="¿Activo?", help_text="Boolean"
    )
    history = HistoricalRecords(inherit=True)

    @classmethod
    def truncate(cls):
        """
        Truncate Table and Restart index. modo de aplicar truncate:
        Model.objects.all().model().truncate()
        """
        TABLE = cls._meta.db_table
        try:
            sql = f"TRUNCATE TABLE {TABLE} RESTART IDENTITY CASCADE;"
            with connection.cursor() as cursor:
                cursor.execute(sql)
        except Exception as e:
            error = str(e)
            print(f"Error en el truncado de tablas: {error}")

    class Meta:
        abstract = True
        ordering = ["-id"]
