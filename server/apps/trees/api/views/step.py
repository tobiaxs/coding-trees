"""Step model related views."""

from rest_framework import viewsets

from server.apps.trees.api.mixins import SerializerPerActionMixin
from server.apps.trees.api.permissions import IsSuperuserOrReadOnly
from server.apps.trees.api.serializers.step import (
    StepInputSerializer,
    StepModelSerializer,
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
        "create": StepInputSerializer,
        "update": StepInputSerializer,
        "partial_update": StepInputSerializer,
    }
    permission_classes = (IsSuperuserOrReadOnly,)

    def perform_create(self, serializer: StepInputSerializer) -> None:
        """Create a new Step instance using the step service.

        Args:
            serializer (StepInputSerializer): serializer holding
                validated data.
        """
        payload = StepCreatePayload(
            creator=self.request.user,
            **serializer.validated_data,
        )
        StepService.create_step_for_path(payload)

    def perform_update(self, serializer: StepInputSerializer) -> None:
        """Update an existing Step instance using the step service.

        Args:
            serializer (StepInputSerializer): serializer holding
                validated data.
        """
        payload = StepUpdatePayload(**serializer.validated_data)
        StepService.update_step(serializer.instance, payload)
