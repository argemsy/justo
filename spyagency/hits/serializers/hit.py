from django.db import transaction
from django.db.models import Q
from django.urls import reverse
from hits.models import Hit, Target
from rest_framework import serializers as sz
from users.models import User


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
    assigned_at = sz.SerializerMethodField()
    buttons = sz.SerializerMethodField()
    buttons_bulk = sz.SerializerMethodField()
    modal = sz.SerializerMethodField()
    rol = sz.SerializerMethodField()

    radio_template = """<div class="custom-control custom-radio m-t-5 pull-{orientacion}">
          <input
            type="radio"
            id="{id}"
            name="customRadio"
            class="custom-control-input m-t-5"
            value="{value}"
            {disabled}
          />
          <label
            class="custom-control-label text-{color} text-bold"
            for="{id}"
            ><b>{label}</b></label
          >
        </div>"""

    select_template = """
    <div class="row form-group m-b-10">
        <label class="col-md-3 col-form-label">{label}</label>
        <select name="{id}" id="{id}" {disabled} class="form-control select2" style="width: 100%;">
            <option disabled selected>{label}</option>
            {options}
        </select>
    </div>"""

    option = """<option value="{value}">{key}</option>"""

    def __init__(self, *args, **kwargs):
        fields = kwargs["context"].pop("fields_out", [])
        super().__init__(*args, **kwargs)
        if fields:
            for field in fields:
                self.fields.pop(field)

    def get_rol(self, instance):
        return instance.assigned_by.get_rol_name

    def get_code_hit(self, instance):
        return instance.code_hit

    def get_hitmen(self, instance):
        hitmen = instance.hitmen
        if hitmen:
            return f"{hitmen.email} | {hitmen.get_team_name}"
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

    def get_assigned_at(self, instance):
        assigned_at = instance.pub_date
        return assigned_at.strftime("%d-%m-%Y")

    def get_buttons(self, instance):
        url_detail = reverse("hits:views:detail", kwargs={"pk": instance.pk})
        return f"""<a href="{url_detail}"><i class="fa fa-eye"></i></a>"""

    def get_buttons_bulk(self, instance):
        pk = instance.pk
        return f"""<a href="javascript:;" onclick="return loadModal({pk});"><i class="fa fa-edit"></i></a>"""

    def get_modal(self, instance):
        html = ""
        status = instance.status
        # radio button 1
        radio = {
            "id": "bad",
            "label": "Finalizar sin éxito",
            "color": "danger",
            "orientacion": "left",
            "value": 3,
        }
        # radio button 2
        radio2 = {
            "id": "good",
            "label": "Finalizar con éxito",
            "color": "primary",
            "orientacion": "right",
            "value": 2,
        }

        user = self.context["request"].user
        if status in [2, 3]:
            radio["disabled"] = "disabled"
            radio2["disabled"] = "disabled"
        elif status == 1:
            radio["disabled"] = ""
            radio2["disabled"] = ""

        if user.get_rol_name in ["Big Boss", "Manager"]:
            if status == 1:
                data_select = {"id": "hitmen", "label": "Asesinos", "disabled": "", "options": self.my_team(instance)}
            elif status in [2, 3]:
                data_select = {
                    "id": "hitmen",
                    "label": "Asesinos",
                    "disabled": "disabled",
                    "options": "",
                }

            html += self.select_template.format(**data_select)
            html += self.radio_template.format(**radio)
            html += self.radio_template.format(**radio2)
        else:
            html += self.radio_template.format(**radio)
            html += self.radio_template.format(**radio2)
        return html

    def my_team(self, instance):
        grupo = self.context["request"].user.get_team_name
        users = User.objects.exclude(pk=instance.hitmen.pk)
        if grupo != "big_boss":
            pk = self.context["request"].user.pk
            grupo = "team-manager-{}".format(str(pk).zfill(3))
            users = users.filter(groups__name=grupo).exclude(
                Q(groups__name="big_boss") | Q(pk__in=[self.context["request"].user.pk, instance.hitmen.pk])
            )
        options = ""
        for user in users:
            options += self.option.format(key=user.email, value=user.pk)
        return options


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
        extra_kwargs = {
            "hitmen": {"required": False}
        }

    def __init__(self, *args, **kwargs):
        fields = kwargs["context"].pop("fields_out", [])
        super().__init__(*args, **kwargs)
        if fields:
            for field in fields:
                self.fields.pop(field)

    def validate_assigned_by(self, assigned_by):
        if not assigned_by.groups.filter(name__in=["big_boss", "managers"]).exists():
            raise sz.ValidationError("Usted no tiene los permisos necesarios para crear un hit.")
        return assigned_by

    def validate_hitmen(self, hitmen):
        if not hitmen:
            hitmen = self.instance.hitmen
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
        if not self.instance:
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

    @transaction.atomic
    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            if value in [None, ""]:
                value = getattr(instance, key)
            setattr(instance, key, value)
        instance.save()
        return super().update(instance, validated_data)
