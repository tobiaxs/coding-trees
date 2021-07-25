"""Create-update services for Step model."""

from typing import Iterable, Optional, TypedDict

from server.apps.trees.models import Option, Path, Solution, Step
from server.apps.users.models import User


class StepCreatePayload(TypedDict):
    """Payload for creating new step."""

    name: str
    creator: User
    is_first: bool
    is_final: bool
    solution: Optional[Solution]
    path: Path
    preceding_options: Iterable[Option]


class StepUpdatePayload(TypedDict):
    """Payload for updating existing step."""

    name: str


class StepService:
    """Handle step create-update operations."""

    @classmethod
    def create_step_for_path(cls, payload: StepCreatePayload) -> Step:
        """Create the step instance with the given payload.

        Args:
            payload (StepCreatePayload): payload containing step data.

        Returns:
            Step: created step instance.
        """
        path = payload.pop("path")
        preceding_options = payload.pop("preceding_options")
        step = Step.objects.create(**payload)
        step.paths.add(path)
        step.preceding_options.set(preceding_options)
        return step

    @classmethod
    def update_step(cls, instance: Step, payload: StepUpdatePayload) -> Step:
        """Update the step instance with the given payload.

        Args:
            instance (Step): current step instance.
            payload (StepUpdatePayload): payload containing new tree data.

        Returns:
            Step: updated step instance.
        """
        instance.name = payload["name"]
        instance.save()
        return instance
