"""Mixin classes for trees API."""

from uuid import UUID

from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import fields, response, serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.request import Request

from server.apps.trees.api.serializers.step import TreeStepModelSerializer
from server.apps.trees.models import Step, Tree
from server.apps.trees.selectors import OptionSelector, StepSelector

extend_step_schema = extend_schema(
    request=inline_serializer("NextStep", {"step": fields.UUIDField()}),
    responses=TreeStepModelSerializer,
)


class SerializerPerActionMixin:
    """Allow different serializers classes per action."""

    action: str
    serializer_classes: dict[str, type[serializers.Serializer]]

    def get_serializer_class(
        self,
    ) -> type[serializers.Serializer]:
        """Based on the action, return the serializer class.

        Returns:
            type[Serializer]: serializer class.
        """
        return self.serializer_classes.get(
            self.action,
            self.serializer_classes["default"],
        )


class TreeStepsMixin:
    """Add step selection actions to a tree view."""

    @extend_step_schema
    @action(detail=True, methods=["get"])
    def first_step(
        self: viewsets.ModelViewSet,
        request: Request,
        pk: UUID,
    ) -> response.Response:
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
    def change_step(
        self: viewsets.ModelViewSet,
        request: Request,
        pk: UUID,
    ) -> response.Response:
        """Return response with the step for specific tree.

        Request data contains the pk of the step to be serialized.

        Args:
            request (Request): incomming request.
            pk (UUID): primary key of the tree.

        Returns:
            Response: response with serialized step and its options,
                or solution if it's the last step.
        """
        tree = self.get_object()
        step = Step.objects.get(pk=request.data["step"])
        step_data = self._build_step_data(tree, step)
        serializer = TreeStepModelSerializer(step_data)
        return response.Response(
            status=status.HTTP_200_OK,
            data=serializer.data,
        )

    def _build_step_data(self, tree: Tree, step: Step) -> dict:
        """Return a dictionary with the step data.

        Args:
            tree (Tree): tree object.
            step (Step): step to serialize.

        Returns:
            dict: serialized step data.
        """
        step_data = {"name": step.name}
        if step.is_final:
            step_data["solution"] = step.solution
        else:
            step_data["options"] = OptionSelector.for_step_name_and_tree(
                step.name,
                tree,
            )
        return step_data
