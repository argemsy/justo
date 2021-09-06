from django.db import transaction
from django.urls import reverse
from rest_framework import serializers as sz

from hits.models import Hit, Target


class HitListSerializer(sz.Serializer):
    id = sz.IntegerField()
    code_hit = sz.SerializerMethodField()
    hitmen = sz.SerializerMethodField()
    target = sz.SerializerMethodField()
    status = sz.SerializerMethodField()
    level = sz.SerializerMethodField()
    hit_detail = sz.SerializerMethodField()
    status_detail = sz.SerializerMethodField()
    assigned_by = sz.SerializerMethodField()
    buttons = sz.SerializerMethodField()

    def get_code_hit(self, instance):
        return instance.code_hit

    def get_hitmen(self, instance):
        hitmen = instance.hitmen
        if hitmen:
            return hitmen.email
        else:
            return "---"

    def get_target(self, instance):
        target = instance.target
        if target:
            return f"""<a data-click="panel-lateral" data-id="{instance.id}" data-panel="panel_target">
                            {target.first_name}, {target.last_name}
                    </a>"""
        else:
            return "No hay datos sobre quién es el encargado de este hit."

    def get_status(self, instance):
        return instance.get_status_display()

    def get_level(self, instance):
        return instance.get_level_display()

    def get_hit_detail(self, instance):
        hit_detail = instance.hit_detail
        if hit_detail not in ["", None]:
            return hit_detail
        else:
            return "No hay detalle para el hit."

    def get_status_detail(self, instance):
        status_detail = instance.status_detail
        if status_detail not in ["", None]:
            return status_detail
        else:
            return "No hay detalle para el status."

    def get_assigned_by(self, instance):
        assigned_by = instance.assigned_by
        if assigned_by:
            return f"{assigned_by.get_rol_name} - {assigned_by.email}"
        else:
            return "No hay datos sobre quíen asigno este hit"

    def get_buttons(self, instance):
        url_detail = reverse("hits:views:detail", kwargs={"pk": instance.pk})
        return f"""<a href="{url_detail}"><i class="fa fa-eye"></i></a>"""


class HitCreateSerializer(sz.ModelSerializer):
    first_name = sz.CharField(write_only=True)
    last_name = sz.CharField(write_only=True)
    assigned_by = sz.HiddenField(
        default=sz.CurrentUserDefault(),
    )

    class Meta:
        model = Hit
        fields = (
            "hitmen",
            "first_name",
            "last_name",
            "level",
            "hit_detail",
            "assigned_by",
        )

    def validate_assigned_by(self, assigned_by):
        if not assigned_by.groups.filter(name__in=["big_boss", "managers"]).exists():
            raise sz.ValidationError(
                "Usted no tiene los permisos necesarios para crear un hit."
            )
        return assigned_by

    def validate_hitmen(self, hitmen):
        if hitmen.died:
            raise sz.ValidationError("El Asesino está fallecido.")
        if hitmen.retired:
            raise sz.ValidationError("El Asesino está retirado.")
        if hitmen == self.context["request"].user:
            raise sz.ValidationError("Usted no se puede asignar misiones.")
        return hitmen

    def validate_hit_detail(self, hit_detail):
        if not hit_detail or hit_detail == "":
            raise sz.ValidationError("Debe agregar una breve descripción del hit.")
        if len(hit_detail) < 15:
            raise sz.ValidationError("Longitud mínima, 15 caracteres.")
        return hit_detail

    def validate(self, attrs):
        nom = attrs.get("first_name", None)
        apellido = attrs.get("last_name", None)
        if not nom or nom == "":
            raise sz.ValidationError("Nombre es un campo requerido")
        if not apellido or apellido == "":
            raise sz.ValidationError("Apellido es un campo requerido")
        if len(nom) < 3 or len(apellido) < 2:
            raise sz.ValidationError("El campo nombre y apellido deben ser válidos.")
        return super().validate(attrs)

    @transaction.atomic
    def createTarget(self, **data):
        target = Target(**data)
        target.created_by = self.context["request"].user
        target.save()
        return target

    @transaction.atomic
    def create(self, validated_data):
        user_data = {
            "first_name": validated_data.pop("first_name"),
            "last_name": validated_data.pop("last_name"),
        }
        target = self.createTarget(**user_data)
        hit = Hit(**validated_data)
        hit.target = target
        hit.save()
        return hit
