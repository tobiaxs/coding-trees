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


class StepCreateSerializer(serializers.Serializer):
    """Write only step serializer for creating instances."""

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

    def validate(self, data: dict) -> dict:
        """Check the model constrains.

        Args:
            data (dict): data to validate.

        Raises:
            ValidationError: if step is both first and final,
                if solution is set on non-final step,
                or there is no solution on final step.

        Returns:
            dict: data after validation.
        """
        if data["is_first"] and data["is_final"]:
            raise serializers.ValidationError(
                "A step cannot be both first and final.",
            )
        if data["is_final"] == (data.get("solution") is None):
            raise serializers.ValidationError(
                "A solution can only be (and has to be) set on the final step.",
            )
        return data

    class Meta:
        fields = (
            "name",
            "is_first",
            "is_final",
            "solution",
            "paths",
        )


class StepUpdateSerializer(serializers.Serializer):
    """Write only step serializer for updating instances."""

    name = serializers.CharField(max_length=NAME_MAX_LENGTH)

    class Meta:
        fields = ("name",)
