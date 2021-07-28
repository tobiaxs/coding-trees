"""Create-update services for Option model."""

from typing import TypedDict

from server.apps.trees.models import Option, Step
from server.apps.users.models import User


class OptionCreatePayload(TypedDict):
    """Payload for creating new option."""

    name: str
    creator: User
    step: Step
    next_step: Step


class OptionUpdatePayload(TypedDict):
    """Payload for updating existing option."""

    name: str
    step: Step
    next_step: Step


class OptionService:
    """Handle option create-update operations."""

    @classmethod
    def create_option(cls, payload: OptionCreatePayload) -> Option:
        """Create the option instance with the given payload.

        Args:
            payload (OptionCreatePayload): payload containing option data.

        Returns:
            Option: created option instance.
        """
        return Option.objects.create(**payload)

    @classmethod
    def update_option(
        cls,
        instance: Option,
        payload: OptionUpdatePayload,
    ) -> Option:
        """Update the option instance with the given payload.

        Args:
            instance (Option): current option instance.
            payload (OptionUpdatePayload): payload containing new option data.

        Returns:
            Option: updated option instance.
        """
        instance.name = payload["name"]
        instance.step = payload["step"]
        instance.next_step = payload.get("next_step")
        instance.save()
        return instance
