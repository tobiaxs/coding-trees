"""Create-update services for Tree model."""

from typing import Iterable, TypedDict

from server.apps.trees.models import Path, Tree
from server.apps.users.models import User


class TreeCreatePayload(TypedDict):
    """Payload for creating new tree."""

    name: str
    creator: User


class TreeUpdatePayload(TypedDict):
    """Payload for updating existing tree."""

    name: str
    paths: Iterable[Path]


class TreeService:
    """Handle tree create-update operations."""

    @classmethod
    def create_tree(cls, payload: TreeCreatePayload) -> Tree:
        """Create the tree instance with the given payload.

        Args:
            payload (TreeCreatePayload): payload containing tree data.

        Returns:
            Tree: created tree instance.
        """
        return Tree.objects.create(**payload)

    @classmethod
    def update_tree(cls, instance: Tree, payload: TreeUpdatePayload) -> Tree:
        """Update the tree instance with the given payload.

        Args:
            instance (Tree): current tree instance.
            payload (TreeUpdatePayload): payload containing new tree data.

        Returns:
            Tree: updated tree instance.
        """
        instance.name = payload["name"]
        instance.save()
        instance.paths.set(payload["paths"])
        return instance
