import re
from random import randint

from django.contrib.auth.models import Group
from django.db import transaction
from django.utils.translation import ugettext as _
from rest_framework import serializers as sz
from rest_framework.validators import UniqueValidator
from users.models import User


class UserListSerializer(sz.Serializer):
    id = sz.IntegerField(label="ID", read_only=True)
    username = sz.SerializerMethodField(label="Nombre de usuario")
    email = sz.SerializerMethodField(label="Email")
    team = sz.SerializerMethodField(label="Equipo")
    rol = sz.SerializerMethodField(label="Rol")
    grupos = sz.SerializerMethodField(label="Grupos")
    avatar = sz.SerializerMethodField(label="Avatar")
    status = sz.SerializerMethodField(label="Avatar")
    bio = sz.SerializerMethodField(label="Biografía")

    def get_username(self, instance):
        return instance.email

    def get_email(self, instance):
        return instance.email

    def get_team(self, instance):
        return instance.get_team_name

    def get_rol(self, instance):
        return instance.get_rol_name

    def get_grupos(self, instance):
        return instance.groups.all().values_list("name", flat=True)

    def get_avatar(self, instance):
        return instance.avatar.url

    def get_status(self, instance):

        if bool(not instance.died or not instance.retired):
            return "Activo"
        else:
            return "Inactivo"

    def get_bio(self, instance):
        return instance.bio if instance.bio else ""


class UserCreateSerializer(sz.ModelSerializer):
    password = sz.CharField(write_only=True, label="Contraseña")
    email = sz.CharField(
        validators=[UniqueValidator(queryset=User.objects.all(), message="Email, este campo debe ser único")]
    )

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "password",
        )
        extra_kwargs = {"email": {"label": "Email"}}

    def validate_email(self, email):
        regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
        if not re.fullmatch(regex, email):
            raise sz.ValidationError("Email Inválido")
        return email

    # def validate_password(self, password):
    #     pattern = r"^(?=.*[\d])(?=.*[A-Z])(?=.*[a-z])(?=.*[@#$])[\w\d@#$]{6,12}$"
    #     print(re.fullmatch(pattern, password))
    #     if not re.fullmatch(pattern, password):
    #         raise sz.ValidationError(
    #             _(
    #                 "La contraseña debe contener una letra mayúscula, una minuscula,\
    #                 un número y al menos un caracter especial."
    #             )
    #         )
    #     return password

    @transaction.atomic
    def create(self, validated_data):
        email = validated_data.pop("email")
        data = {
            "username": email,
            "email": email,
            "password": validated_data.pop("password"),
            "is_staff": True,
            "is_active": True,
        }
        user = User.objects.create_user(**data)
        grupos = Group.objects.filter(name__istartswith="team-manager-")
        nro_grupos = grupos.count()
        id_groups = randint(0, (nro_grupos - 1))
        user.groups.add(grupos[id_groups])
        return user
