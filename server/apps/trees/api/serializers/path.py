"""Path model related serializers."""

from rest_framework import serializers

from server.apps.trees.api.serializers.step import StepModelSerializer
from server.apps.trees.models import NAME_MAX_LENGTH, Path


class PathModelSerializer(serializers.ModelSerializer):
    """Read only path model serializer with nested instances."""

    steps = StepModelSerializer(many=True, read_only=True, required=False)

    class Meta:
        model = Path
        fields = (
            "pk",
            "name",
            "steps",
            "creator",
        )


class PathInputSerializer(serializers.Serializer):
    """Write only path serializer."""

    name = serializers.CharField(max_length=NAME_MAX_LENGTH)

    class Meta:
        fields = ("name",)
