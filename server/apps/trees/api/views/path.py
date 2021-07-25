"""Path model related views."""

from rest_framework import viewsets

from server.apps.trees.api.mixins import SerializerPerActionMixin
from server.apps.trees.api.permissions import IsSuperuserOrReadOnly
from server.apps.trees.api.serializers.path import (
    PathInputSerializer,
    PathModelSerializer,
)
from server.apps.trees.models import Path
from server.apps.trees.services.path import (
    PathCreatePayload,
    PathService,
    PathUpdatePayload,
)


class PathViewSet(
    SerializerPerActionMixin,
    viewsets.ModelViewSet,
):
    """Crud viewset for Path model."""

    queryset = Path.objects.all()
    serializer_classes = {
        "default": PathModelSerializer,
        "create": PathInputSerializer,
        "update": PathInputSerializer,
        "partial_update": PathInputSerializer,
    }
    permission_classes = (IsSuperuserOrReadOnly,)

    def perform_create(self, serializer: PathInputSerializer) -> None:
        """Create a new Path instance using the path service.

        Args:
            serializer (PathInputSerializer): serializer holding validated data.
        """
        payload = PathCreatePayload(
            creator=self.request.user,
            **serializer.validated_data,
        )
        PathService.create_path(payload)

    def perform_update(self, serializer: PathInputSerializer) -> None:
        """Update an existing Path instance using the path service.

        Args:
            serializer (PathInputSerializer): serializer holding validated data.
        """
        payload = PathUpdatePayload(**serializer.validated_data)
        PathService.update_path(serializer.instance, payload)
