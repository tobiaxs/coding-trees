"""Trees app models."""
from typing import Optional

from django.db import models

from server.apps.generic.models import GenericModelWithCreator

NAME_MAX_LENGTH = 63


class Tree(GenericModelWithCreator):
    """Highest level model, containing and grouping several paths."""

    name = models.CharField(max_length=NAME_MAX_LENGTH)
    paths = models.ManyToManyField("Path", related_name="trees", blank=True)

    def __str__(self) -> str:
        """Return the name of the tree.

        Returns:
            str: name.
        """
        return self.name

    class Meta:
        unique_together = ("name", "creator")


class Path(GenericModelWithCreator):
    """Container for all the steps which belong to the tree."""

    name = models.CharField(max_length=NAME_MAX_LENGTH)
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
        final_step = self.steps.filter(is_final=True).first()
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

    name = models.CharField(max_length=NAME_MAX_LENGTH)
    is_first = models.BooleanField(default=False)
    is_final = models.BooleanField(default=False)
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
                check=models.Q(is_first=False) | models.Q(is_final=False),
                name="not_first_and_final",
            ),
            models.CheckConstraint(
                check=(
                    models.Q(is_final=False, solution__isnull=True)
                    | models.Q(is_final=True, solution__isnull=False)
                ),
                name="not_final_with_no_solution",
            ),
        )


class Option(GenericModelWithCreator):
    """Specific option in the step.

    Has to know which step it should lead to.
    """

    name = models.CharField(max_length=NAME_MAX_LENGTH)
    step = models.ForeignKey(
        "Step",
        related_name="options",
        on_delete=models.CASCADE,
    )
    next_step = models.ForeignKey(
        "Step",
        related_name="preceding_options",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
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
                check=~models.Q(step=models.F("next_step")),
                name="steps_not_equal",
            ),
        ]


class Solution(GenericModelWithCreator):
    """Potential solution for given problem.

    It is meant to be a design pattern, or other structural hint.
    """

    name = models.CharField(max_length=NAME_MAX_LENGTH)
    slug = models.TextField()

    def __str__(self) -> str:
        """Return the name of the solution.

        Returns:
            str: name.
        """
        return self.name
