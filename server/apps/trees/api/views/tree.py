"""Tree model related views."""

from uuid import UUID

from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import fields, response, status, viewsets
from rest_framework.decorators import action
from rest_framework.request import Request

from server.apps.trees.api.mixins import SerializerPerActionMixin
from server.apps.trees.api.permissions import IsSuperuserOrReadOnly
from server.apps.trees.api.serializers.step import TreeStepModelSerializer
from server.apps.trees.api.serializers.tree import (
    TreeCreateSerializer,
    TreeModelSerializer,
    TreeUpdateSerializer,
)
from server.apps.trees.models import Step, Tree
from server.apps.trees.selectors import OptionSelector, StepSelector
from server.apps.trees.services.tree import (
    TreeCreatePayload,
    TreeService,
    TreeUpdatePayload,
)

extend_step_schema = extend_schema(
    request=inline_serializer("NextStep", {"step": fields.UUIDField()}),
    responses=TreeStepModelSerializer,
)


class TreeViewSet(
    SerializerPerActionMixin,
    viewsets.ModelViewSet,
):
    """Crud viewset for Tree model."""

    queryset = Tree.objects.all()
    serializer_classes = {
        "default": TreeModelSerializer,
        "create": TreeCreateSerializer,
        "update": TreeUpdateSerializer,
        "partial_update": TreeUpdateSerializer,
    }
    permission_classes = (IsSuperuserOrReadOnly,)

    def perform_create(self, serializer: TreeCreateSerializer) -> None:
        """Create a new Tree instance using the tree service.

        Args:
            serializer (TreeCreateSerializer): serializer holding
                validated data.
        """
        payload = TreeCreatePayload(
            creator=self.request.user,
            **serializer.validated_data,
        )
        TreeService.create_tree(payload)

    def perform_update(self, serializer: TreeUpdateSerializer) -> None:
        """Update an existing Tree instance using the tree service.

        Args:
            serializer (TreeUpdateSerializer): serializer holding
                validated data.
        """
        payload = TreeUpdatePayload(**serializer.validated_data)
        TreeService.update_tree(serializer.instance, payload)

    @extend_step_schema
    @action(detail=True, methods=["get"])
    def first_step(self, request: Request, pk: UUID) -> response.Response:
        """Return response with the first step and its options for specific tree.

        Args:
            request (Request): incomming request.
            pk (UUID): primary key of the tree.

        Returns:
            Response: response with serialized first step and its options.
        """
        tree = self.get_object()
        first_step_name = StepSelector.first_name_for_tree(tree)
        if first_step_name:
            step_data = {
                "name": first_step_name,
                "options": OptionSelector.for_step_name_and_tree(
                    first_step_name,
                    tree,
                ),
            }
            data = TreeStepModelSerializer(step_data).data
        else:
            data = {}
        return response.Response(
            status=status.HTTP_200_OK,
            data=data,
        )

    @extend_step_schema
    @action(detail=True, methods=["post"])
    def next_step(self, request: Request, pk: UUID) -> response.Response:
        """Return response with the step and its options for specific tree.

        Request data contains the pk of the step to be serialized.

        Args:
            request (Request): incomming request.
            pk (UUID): primary key of the tree.

        Returns:
            Response: response with serialized step and its options.
        """
        tree = self.get_object()
        step = Step.objects.get(pk=request.data["step"])
        step_data = {
            "name": step.name,
            "options": OptionSelector.for_step_name_and_tree(
                step.name,
                tree,
            ),
        }
        serializer = TreeStepModelSerializer(step_data)
        return response.Response(
            status=status.HTTP_200_OK,
            data=serializer.data,
        )
