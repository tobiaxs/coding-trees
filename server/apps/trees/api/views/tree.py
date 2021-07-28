"""Tree model related views."""

from rest_framework import viewsets

from server.apps.trees.api.mixins import SerializerPerActionMixin
from server.apps.trees.api.permissions import IsSuperuserOrReadOnly
from server.apps.trees.api.serializers.tree import (
    DecisionTreeModelSerializer,
    TreeCreateSerializer,
    TreeModelSerializer,
    TreeUpdateSerializer,
)
from server.apps.trees.models import Tree
from server.apps.trees.services.tree import (
    TreeCreatePayload,
    TreeService,
    TreeUpdatePayload,
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


class DecisionTreeViewSet(viewsets.ReadOnlyModelViewSet):
    """Read only viewset for simulating decision trees."""

    queryset = Tree.objects.all()
    serializer_class = DecisionTreeModelSerializer
