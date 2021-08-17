"""Step model related views."""

from rest_framework import viewsets

from server.apps.trees.api.mixins import SerializerPerActionMixin
from server.apps.trees.api.permissions import IsSuperuserOrReadOnly
from server.apps.trees.api.serializers.step import (
    StepCreateSerializer,
    StepModelSerializer,
    StepUpdateSerializer,
)
from server.apps.trees.models import Step
from server.apps.trees.services.step import (
    StepCreatePayload,
    StepService,
    StepUpdatePayload,
)


class StepViewSet(
    SerializerPerActionMixin,
    viewsets.ModelViewSet,
):
    """Crud viewset for Step model."""

    queryset = Step.objects.all()
    serializer_classes = {
        "default": StepModelSerializer,
        "create": StepCreateSerializer,
        "update": StepUpdateSerializer,
        "partial_update": StepUpdateSerializer,
    }
    permission_classes = (IsSuperuserOrReadOnly,)

    def perform_create(self, serializer: StepCreateSerializer) -> None:
        """Create a new Step instance using the step service.

        Args:
            serializer (StepCreateSerializer): serializer holding
                validated data.
        """
        payload = StepCreatePayload(**serializer.validated_data)
        instance = StepService.create_step_for_path(payload)
        serializer.validated_data["pk"] = instance.pk

    def perform_update(self, serializer: StepUpdateSerializer) -> None:
        """Update an existing Step instance using the step service.

        Args:
            serializer (StepUpdateSerializer): serializer holding
                validated data.
        """
        payload = StepUpdatePayload(**serializer.validated_data)
        StepService.update_step(serializer.instance, payload)
