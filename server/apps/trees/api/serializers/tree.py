"""Tree model related serializers."""

from rest_framework import serializers

from server.apps.trees.api.serializers.path import PathModelSerializer
from server.apps.trees.models import NAME_MAX_LENGTH, Path, Tree


class TreeModelSerializer(serializers.ModelSerializer):
    """Read only tree model serializer with nested instances."""

    paths = PathModelSerializer(many=True, read_only=True)

    class Meta:
        model = Tree
        fields = (
            "pk",
            "name",
            "paths",
        )


class TreeCreateSerializer(serializers.Serializer):
    """Write only tree serializer for creating instances."""

    name = serializers.CharField(max_length=NAME_MAX_LENGTH)

    class Meta:
        fields = ("name",)


class TreeUpdateSerializer(serializers.Serializer):
    """Write only tree serializer for updating instances."""

    name = serializers.CharField(max_length=NAME_MAX_LENGTH)
    paths = serializers.PrimaryKeyRelatedField(
        queryset=Path.objects.all(),
        many=True,
        required=False,
        allow_null=True,
    )

    class Meta:
        fields = ("name", "paths")
