from rest_framework.viewsets import ModelViewSet

from hits.models import Target
from hits.serializers import TargetSerializer


class TargetViewSet(ModelViewSet):
    queryset = Target.objects.all()
    serializer_class = TargetSerializer
