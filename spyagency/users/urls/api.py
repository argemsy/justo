from rest_framework.routers import DefaultRouter

from users.apis import UserViewSet

router = DefaultRouter()

router.register("", UserViewSet, "user")
