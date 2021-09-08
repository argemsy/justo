from django.contrib.auth.models import Group
from django.db.models import Q
from django.urls import reverse
from django.utils.decorators import method_decorator
from hits.models import Hit
from hits.serializers import HitCreateSerializer, HitListSerializer
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from users.models import User
from utils.decorator import decorator_api_titles


@method_decorator(decorator_api_titles(title="Hit's", subtitle="Listado general"), name="list")
@method_decorator(decorator_api_titles(title="Hit", subtitle="Detalle"), name="retrieve")
@method_decorator(decorator_api_titles(title="Re-Asignaciones", subtitle=""), name="bulk")
class HitViewSet(ModelViewSet):
    serializer_class = HitCreateSerializer

    def get_big_boss(self):
        big_boss = User.objects.filter(groups__name__in=["big_boss"])
        return big_boss

    def get_queryset(self):
        if self.request.user.groups.filter(name="big_boss").exists():
            queryset = Hit.objects.all()
        elif self.request.user.groups.filter(name="managers").exists():
            queryset = Hit.objects.filter(
                Q(assigned_by=self.request.user) | Q(hitmen=self.request.user) | Q(assigned_by__in=self.get_big_boss())
            )
        else:
            queryset = Hit.objects.filter(hitmen=self.request.user)
        return queryset

    def list(self, request, *args, **kwargs):
        create_url = reverse("hits:views:create")
        context = super().list(request, *args, **kwargs)
        if self.request.user.groups.filter(name__in=["big_boss", "managers"]).exists():
            context.data["create_url"] = create_url
        else:
            context.data["create_url"] = None
        return context

    @action(methods=["GET"], detail=False)
    def bulk(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.action in ["list", "retrieve", "bulk"]:
            return HitListSerializer
        return super().get_serializer_class()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        if self.action == "list":
            context["fields_out"] = ["hit_detail", "status_detail", "assigned_at", "modal", "buttons_bulk"]
        elif self.action == "retrieve":
            context["fields_out"] = ["id", "buttons", "status_detail", "level", "buttons_bulk"]
        elif self.action == "bulk":
            context["fields_out"] = ["hit_detail", "status_detail", "assigned_at", "modal", "buttons"]
        elif self.action == "update":
            if self.request.user.get_rol_name in ["Big Boss", "Manager"] and self.get_object().status == 1:
                context["fields_out"] = ["first_name", "last_name"]
            elif self.request.user.get_rol_name in ["Big Boss", "Manager"] and self.get_object().status in [2, 3]:
                context["fields_out"] = ["first_name", "last_name", "hitmen"]
            elif self.request.user.get_rol_name not in ["Big Boss", "Manager"] and self.get_object().status == 1:
                context["fields_out"] = ["first_name", "last_name", "hitmen"]
        return context

    def perform_update(self, serializer):
        instance_status = self.get_object().status
        status = self.request.POST.get("status", instance_status)
        extra_data = {"status": status}
        serializer.save(**extra_data)
        return super().perform_update(serializer)
