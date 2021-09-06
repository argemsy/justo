"""
Sección administrativa del modelo cuenta
"""
# Librerias Django
from django.contrib import admin
from django.contrib.admin.models import LogEntry
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

# Librerias en carpetas locales
# from .forms import PersonaChangeForm, PersonaCreationForm
from users.models import User  # , Archivo


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ("username", "rol", "team")
    fieldsets = (
        ("Usuario", {"fields": ("avatar", "username", "rol")}),
        (
            "Información personal",
            {
                "classes": ("collapse",),
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                    "gender",
                ),
            },
        ),
        (
            "Permisos",
            {
                "classes": ("collapse",),
                "fields": (
                    "is_superuser",
                    "is_staff",
                    "is_active",
                    "password",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (
            "Seguimiento",
            {
                "classes": ("collapse",),
                "fields": (
                    "died",
                    "died_date",
                    "retired",
                    "retired_date",
                ),
            },
        ),
        (
            "Auditoria",
            {
                "classes": ("collapse",),
                "fields": (
                    "last_login",
                    "date_joined",
                ),
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "email",
                    "password1",
                    "password2",
                ),
            },
        ),
    )

    search_fields = ("email",)
    list_filter = ("is_staff", "is_superuser")
    # list_display = ('__str__', 'username', 'email',)
    # list_select_related = ()
    show_full_result_count = False
    actions_selection_counter = False
    ordering = ("id",)
    readonly_fields = ("rol", "team")

    def rol(self, instance):
        return instance.get_rol_name

    rol.short_description = "Rol"

    def team(self, instance):
        return instance.get_team_name

    team.short_description = "Nombre de mi Equipo"

    # def dream_team(self, instance):
    #     return instance.get_people_team
    # dream_team.short_description = 'Integrantes de mi equipo'


admin.site.register(LogEntry)
