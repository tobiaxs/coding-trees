"""Trees app models."""

from django.core.exceptions import ValidationError
from django.db import models
from martor.models import MartorField
from structlog import get_logger

from server.apps.generic.models import GenericModelWithCreator

NAME_MAX_LENGTH = 63

# TODO: Step and Option don't need a creator anymore.

log = get_logger()


class Tree(GenericModelWithCreator):
    """Highest level model, containing and grouping several paths."""

    name = models.CharField(max_length=NAME_MAX_LENGTH)
    paths = models.ManyToManyField("Path", related_name="trees", blank=True)
    # TODO: Add inconsistencies model.

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
    path = models.ForeignKey(
        "Path",
        on_delete=models.CASCADE,
        related_name="steps",
    )
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

    def clean(self) -> None:
        """Check the fields on the python level.

        Raises:
            ValidationError: if step is both first and final,
                if solution is set on non-final step,
                or there is no solution on final step.
        """
        if self.is_first and self.is_final:
            log.error(
                "Step is both first and final.",
                name=self.name,
                creator=self.creator.email,
            )
            raise ValidationError("A step cannot be both first and final.")
        if self.is_final == (self.solution is None):
            log.error(
                "Solution is not on the final step.",
                name=self.name,
                creator=self.creator.email,
            )
            raise ValidationError(
                "A solution can only be (and has to be) set on the final step.",
            )

    class Meta:
        unique_together = ("name", "path")
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

    def clean(self) -> None:
        """Check the fields on the python level.

        Raises:
            ValidationError: if the steps are equal.
        """
        if self.step == self.next_step:
            log.error(
                "Steps are equal.",
                name=self.name,
                creator=self.creator.email,
            )
            raise ValidationError(
                "A step cannot be the same as the next step.",
            )

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
    description = MartorField()

    def __str__(self) -> str:
        """Return the name of the solution.

        Returns:
            str: name.
        """
        return self.name
