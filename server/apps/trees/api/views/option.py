"""Option model related views."""

from rest_framework import viewsets

from server.apps.trees.api.mixins import SerializerPerActionMixin
from server.apps.trees.api.permissions import IsSuperuserOrReadOnly
from server.apps.trees.api.serializers.option import (
    OptionCreateSerializer,
    OptionModelSerializer,
    OptionUpdateSerializer,
)
from server.apps.trees.models import Option
from server.apps.trees.services.option import (
    OptionCreatePayload,
    OptionService,
    OptionUpdatePayload,
)


class OptionViewSet(
    SerializerPerActionMixin,
    viewsets.ModelViewSet,
):
    """Crud viewset for Option model."""

    queryset = Option.objects.all()
    serializer_classes = {
        "default": OptionModelSerializer,
        "create": OptionCreateSerializer,
        "update": OptionUpdateSerializer,
        "partial_update": OptionUpdateSerializer,
    }
    permission_classes = (IsSuperuserOrReadOnly,)

    def perform_create(self, serializer: OptionCreateSerializer) -> None:
        """Create a new Option instance using the option service.

        Args:
            serializer (OptionCreateSerializer): serializer holding
                validated data.
        """
        payload = OptionCreatePayload(**serializer.validated_data)
        instance = OptionService.create_option(payload)
        serializer.validated_data["pk"] = instance.pk

    def perform_update(self, serializer: OptionUpdateSerializer) -> None:
        """Update an existing Option instance using the option service.

        Args:
            serializer (OptionUpdateSerializer): serializer holding
                validated data.
        """
        payload = OptionUpdatePayload(**serializer.validated_data)
        OptionService.update_option(serializer.instance, payload)
