"""Option model related views."""

from rest_framework import viewsets

from server.apps.trees.api.mixins import SerializerPerActionMixin
from server.apps.trees.api.permissions import IsSuperuserOrReadOnly
from server.apps.trees.api.serializers.option import (
    OptionInputSerializer,
    OptionModelSerializer,
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
        "create": OptionInputSerializer,
        "update": OptionInputSerializer,
        "partial_update": OptionInputSerializer,
    }
    permission_classes = (IsSuperuserOrReadOnly,)

    def perform_create(self, serializer: OptionInputSerializer) -> None:
        """Create a new Option instance using the option service.

        Args:
            serializer (OptionInputSerializer): serializer holding
                validated data.
        """
        payload = OptionCreatePayload(
            creator=self.request.user,
            **serializer.validated_data,
        )
        OptionService.create_option(payload)

    def perform_update(self, serializer: OptionInputSerializer) -> None:
        """Update an existing Option instance using the option service.

        Args:
            serializer (OptionInputSerializer): serializer holding
                validated data.
        """
        payload = OptionUpdatePayload(**serializer.validated_data)
        OptionService.update_option(serializer.instance, payload)
