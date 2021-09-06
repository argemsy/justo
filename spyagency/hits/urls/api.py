from hits.apis import HitViewSet, TargetViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()


router.register("targets", TargetViewSet, "target")
router.register("hits", HitViewSet, "hit")
