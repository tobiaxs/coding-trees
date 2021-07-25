"""Step model related serializers."""

from rest_framework import serializers

from server.apps.trees.api.serializers.option import OptionModelSerializer
from server.apps.trees.api.serializers.solution import SolutionModelSerializer
from server.apps.trees.models import (
    NAME_MAX_LENGTH,
    Option,
    Path,
    Solution,
    Step,
)


class StepModelSerializer(serializers.ModelSerializer):
    """Read only step model serializer with nested instances."""

    solution = SolutionModelSerializer(read_only=True, required=False)
    options = OptionModelSerializer(many=True, read_only=True)

    class Meta:
        model = Step
        fields = (
            "pk",
            "name",
            "is_first",
            "is_final",
            "solution",
            "options",
            "creator",
        )


class StepInputSerializer(serializers.Serializer):
    """Write only step serializer."""

    name = serializers.CharField(max_length=NAME_MAX_LENGTH)
    is_first = serializers.BooleanField(default=False)
    is_final = serializers.BooleanField(default=False)
    solution = serializers.PrimaryKeyRelatedField(
        queryset=Solution.objects.all(),
        required=False,
        allow_null=True,
    )
    path = serializers.PrimaryKeyRelatedField(queryset=Path.objects.all())
    preceding_options = serializers.PrimaryKeyRelatedField(
        queryset=Option.objects.all(),
        many=True,
        required=False,
        allow_null=True,
    )

    class Meta:
        fields = (
            "name",
            "is_first",
            "is_final",
            "solution",
            "paths",
        )
