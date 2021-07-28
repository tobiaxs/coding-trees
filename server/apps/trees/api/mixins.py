"""Mixin classes for trees API."""

from rest_framework import serializers


class SerializerPerActionMixin:
    """Used to allow for different serializers classes per action."""

    action: str
    serializer_classes: dict[str, type[serializers.Serializer]]

    def get_serializer_class(
        self,
    ) -> type[serializers.Serializer]:
        """Based on the action, return the serializer class.

        Returns:
            type[serializers.Serializer]: serializer class.
        """
        return self.serializer_classes.get(
            self.action,
            self.serializer_classes["default"],
        )
