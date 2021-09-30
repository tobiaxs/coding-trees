"""Solution model related views."""

from rest_framework import viewsets

from server.apps.trees.api.mixins import SerializerPerActionMixin
from server.apps.trees.api.permissions import IsSuperuserOrReadOnly
from server.apps.trees.api.serializers.solution import (
    SolutionInputSerializer,
    SolutionModelSerializer,
)
from server.apps.trees.models import Solution
from server.apps.trees.services.solution import (
    SolutionCreatePayload,
    SolutionService,
    SolutionUpdatePayload,
)


class SolutionViewSet(
    SerializerPerActionMixin,
    viewsets.ModelViewSet,
):
    """Crud viewset for Solution model."""

    queryset = Solution.objects.all()
    serializer_classes = {
        "default": SolutionModelSerializer,
        "create": SolutionInputSerializer,
        "update": SolutionInputSerializer,
        "partial_update": SolutionInputSerializer,
    }
    permission_classes = (IsSuperuserOrReadOnly,)

    def perform_create(self, serializer: SolutionInputSerializer) -> None:
        """Create a new Solution instance using the solution service.

        Args:
            serializer (SolutionInputSerializer): serializer holding
                validated data.
        """
        payload = SolutionCreatePayload(
            creator=self.request.user,
            **serializer.validated_data,
        )
        instance = SolutionService.create_solution(payload)
        serializer.validated_data["pk"] = instance.pk

    def perform_update(self, serializer: SolutionInputSerializer) -> None:
        """Update an existing Solution instance using the solution service.

        Args:
            serializer (SolutionInputSerializer): serializer holding
                validated data.
        """
        payload = SolutionUpdatePayload(**serializer.validated_data)
        SolutionService.update_solution(serializer.instance, payload)
