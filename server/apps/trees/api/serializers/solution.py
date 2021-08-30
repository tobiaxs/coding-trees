"""Solution model related serializers."""

from rest_framework import serializers

from server.apps.trees.models import NAME_MAX_LENGTH, Solution


class SolutionModelSerializer(serializers.ModelSerializer):
    """Read only solution model serializer."""

    author = serializers.CharField(source="creator.username")

    class Meta:
        model = Solution
        fields = (
            "pk",
            "name",
            "description",
            "creator",
            "author",
        )


class SolutionInputSerializer(serializers.Serializer):
    """Write only option serializer."""

    name = serializers.CharField(max_length=NAME_MAX_LENGTH)
    description = serializers.CharField()

    class Meta:
        fields = (
            "name",
            "description",
        )
