from rest_framework import serializers as sz

from hits.models import Target


class TargetSerializer(sz.ModelSerializer):
    created_by = sz.HiddenField(default=sz.CurrentUserDefault())

    class Meta:
        model = Target
        fields = (
            "id",
            "first_name",
            "last_name",
            "extra_info",
            "created_by",
        )
