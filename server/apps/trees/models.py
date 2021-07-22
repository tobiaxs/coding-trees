"""Trees app models."""
from typing import Optional

from django.db import models
from django.db.models.query_utils import F, Q  # noqa: WPS347

from server.apps.generic.models import GenericModelWithCreator


class Tree(GenericModelWithCreator):
    """Highest level model, containing and grouping several paths."""

    name = models.TextField()
    paths = models.ManyToManyField("Path", related_name="trees", blank=True)

    def __str__(self) -> str:
        """Return the name of the tree.

        Returns:
            str: name.
        """
        return self.name


class Path(GenericModelWithCreator):
    """Container for all the steps which belong to the tree."""

    name = models.TextField()
    steps = models.ManyToManyField(
        "Step",
        related_name="paths",
        blank=True,
    )

    @property
    def solution(self) -> Optional["Solution"]:
        """Return solution for the path if the final step exists.

        Returns:
            Optional[Solution]: solution connected to the final step.
        """
        final_step = self.steps.filter(is_final_step=True).first()
        if final_step:
            return final_step.solution
        return None

    def __str__(self) -> str:
        """Return the name of the path.

        Returns:
            str: name.
        """
        return self.name


class Step(GenericModelWithCreator):
    """Contain all the options in some part of the path.

    Final step also contain the solution.
    """

    name = models.TextField()
    is_first_step = models.BooleanField(default=False)
    is_final_step = models.BooleanField(default=False)
    solution = models.ForeignKey(
        "Solution",
        related_name="final_steps",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    def __str__(self) -> str:
        """Return the name of the step.

        Returns:
            str: name.
        """
        return self.name

    class Meta:
        constraints = (
            models.CheckConstraint(
                check=Q(is_first_step=True) & Q(is_final_step=True),
                name="not_first_and_final",
            ),
            models.CheckConstraint(
                check=Q(is_final_step=True) & Q(solution__isnull=True),
                name="not_final_with_no_solution",
            ),
            models.CheckConstraint(
                check=Q(options__isnull=False) & Q(solution__isnull=False),
                name="not_both_options_and_solution",
            ),
        )


class Option(GenericModelWithCreator):
    """Specific option in the step.

    Has to know which step it should lead to.
    """

    name = models.TextField()
    step = models.ForeignKey(
        "Step",
        related_name="options",
        on_delete=models.CASCADE,
    )
    next_step = models.ForeignKey(
        "Step",
        related_name="preceding_options",
        on_delete=models.CASCADE,
    )

    def __str__(self) -> str:
        """Return the name of the option.

        Returns:
            str: name.
        """
        return self.name

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=Q(step=F("next_step")),
                name="steps_not_equal",
            ),
        ]


class Solution(GenericModelWithCreator):
    """Potential solution for given problem.

    It is meant to be a design pattern, or other structural hint.
    """

    name = models.TextField()
    slug = models.TextField()

    def __str__(self) -> str:
        """Return the name of the solution.

        Returns:
            str: name.
        """
        return self.name
