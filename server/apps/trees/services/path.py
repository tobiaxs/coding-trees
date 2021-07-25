"""Create-update services for Path model."""

from typing import TypedDict

from server.apps.trees.models import Path
from server.apps.users.models import User


class PathCreatePayload(TypedDict):
    """Payload for creating new path."""

    name: str
    creator: User


class PathUpdatePayload(TypedDict):
    """Payload for updating existing path."""

    name: str


class PathService:
    """Handle path create-update operations."""

    @classmethod
    def create_path(cls, payload: PathCreatePayload) -> Path:
        """Create the path instance with the given payload.

        Args:
            payload (PathCreatePayload): payload containing path data.

        Returns:
            Path: created path instance.
        """
        return Path.objects.create(**payload)

    @classmethod
    def update_path(cls, instance: Path, payload: PathUpdatePayload) -> Path:
        """Update the path instance with the given payload.

        Args:
            instance (Path): current path instance.
            payload (PathUpdatePayload): payload containing new path data.

        Returns:
            Path: updated path instance.
        """
        instance.name = payload["name"]
        instance.save()
        return instance
