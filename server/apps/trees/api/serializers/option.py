"""Option model related serializers."""

from rest_framework import serializers

from server.apps.trees.models import NAME_MAX_LENGTH, Option, Step


class OptionModelSerializer(serializers.ModelSerializer):
    """Read only option model serializer."""

    class Meta:
        model = Option
        fields = (
            "pk",
            "name",
            "step",
            "next_step",
            "creator",
        )


class OptionInputSerializer(serializers.Serializer):
    """Write only option serializer."""

    name = serializers.CharField(max_length=NAME_MAX_LENGTH)
    step = serializers.PrimaryKeyRelatedField(queryset=Step.objects.all())
    next_step = serializers.PrimaryKeyRelatedField(
        queryset=Step.objects.all(),
        required=False,
        allow_null=True,
    )

    def validate(self, data: dict) -> dict:
        """Check the model constrains.

        Args:
            data (dict): data to validate.

        Raises:
            ValidationError: if the steps are equal.

        Returns:
            dict: data after validation.
        """
        if data["step"] == data.get("next_step"):
            raise serializers.ValidationError(
                "A step cannot be the same as the next step.",
            )
        return data

    class Meta:
        fields = (
            "name",
            "step",
        )
