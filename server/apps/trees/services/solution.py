"""Create-update services for Solution model."""

from typing import TypedDict

from server.apps.trees.models import Solution
from server.apps.users.models import User


class SolutionCreatePayload(TypedDict):
    """Payload for creating new solution."""

    name: str
    creator: User
    slug: str


class SolutionUpdatePayload(TypedDict):
    """Payload for updating existing solution."""

    name: str
    slug: str


class SolutionService:
    """Handle solution create-update operations."""

    @classmethod
    def create_solution(cls, payload: SolutionCreatePayload) -> Solution:
        """Create the solution instance with the given payload.

        Args:
            payload (SolutionCreatePayload): payload containing solution data.

        Returns:
            Solution: created solution instance.
        """
        return Solution.objects.create(**payload)

    @classmethod
    def update_solution(
        cls,
        instance: Solution,
        payload: SolutionUpdatePayload,
    ) -> Solution:
        """Update the solution instance with the given payload.

        Args:
            instance (Solution): current solution instance.
            payload (SolutionUpdatePayload): payload containing
                new solution data.

        Returns:
            Solution: updated solution instance.
        """
        instance.name = payload["name"]
        instance.slug = payload["slug"]
        instance.save()
        return instance
