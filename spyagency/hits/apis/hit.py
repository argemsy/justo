from django.db.models import Q
from django.urls import reverse
from django.utils.decorators import method_decorator
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet

from hits.models import Hit
from hits.serializers import HitCreateSerializer, HitListSerializer
from utils.decorator import decorator_api_titles


@method_decorator(
    decorator_api_titles(title="Hit's", subtitle="Listado general"), name="list"
)
@method_decorator(
    decorator_api_titles(title="Hit", subtitle="Detalle"), name="retrieve"
)
@method_decorator(
    decorator_api_titles(title="Re-Asignaciones", subtitle=""), name="bulk"
)
class HitViewSet(ModelViewSet):
    serializer_class = HitCreateSerializer

    def get_queryset(self):
        if self.request.user.groups.filter(name="big_boss").exists():
            queryset = Hit.objects.all()
        elif self.request.user.groups.filter(name="managers").exists():
            queryset = Hit.objects.filter(
                Q(assigned_by=self.request.user) | Q(hitmen=self.request.user)
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
