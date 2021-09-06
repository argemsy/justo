from django.utils.decorators import method_decorator
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from users.models import User
from users.serializers import UserCreateSerializer, UserListSerializer
from utils.decorator import decorator_api_titles


@method_decorator(decorator_api_titles(title="Hitmen's", subtitle="Listado general"), name="list")
class UserViewSet(ModelViewSet):
    serializer_class = UserListSerializer

    def get_permissions(self):
        if self.action == "create":
            return [AllowAny()]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action in ["create", "update"]:
            return UserCreateSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        if self.request.user.groups.filter(name="big_boss").exists():
            return User.objects.all().exclude(pk=1)
        elif self.request.user.groups.filter(name="managers").exists():
            group_name = "team-manager-{}".format(str(self.request.user.pk).zfill(3))
            queryset = User.objects.filter(groups__name=group_name).exclude(pk=1)
        else:
            queryset = User.objects.none()
        return queryset

    @action(methods=["GET"], detail=False)
    def profile(self, request, *args, **kwargs):
        self.object = self.request.user
        serializer = UserListSerializer(self.object, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
