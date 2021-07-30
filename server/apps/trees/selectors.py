"""Selector classes for tree app models."""

from typing import Optional

from django.db.models import Count
from django.db.models.query import QuerySet

from server.apps.trees.models import Option, Path, Solution, Step, Tree


class StepSelector:
    """Handle step fetching operations."""

    @classmethod
    def first_name_for_tree(cls, tree: Tree) -> Optional[str]:
        """Return name of first step for a tree.

        First step is considered to be 'is_first' with the most options
        for the same name.

        Args:
            tree (Tree): tree to get step for.

        Returns:
            str: name of the step that is first
                and will return the most options.
        """
        step_name_and_count = (
            Step.objects.filter(path__trees=tree, is_first=True)
            .values("name")
            .annotate(options_count=Count("options"))
            .order_by("-options_count")
        ).first()

        if step_name_and_count:
            return step_name_and_count["name"]
        return None


class OptionSelector:
    """Handle option fetching operations."""

    @classmethod
    def for_step_name_and_tree(cls, step_name: str, tree: Tree) -> QuerySet:
        """Return all options for a given step name and tree.

        Args:
            step_name (str): name of the step.
            tree (Tree): tree of the path that has the step.

        Returns:
            QuerySet: all options for the step and tree.
        """
        return Option.objects.filter(
            step__name=step_name,
            step__path__trees=tree,
        )


class SolutionSelector:
    """Handle solution fetching operations."""

    @classmethod
    def for_path(cls, path: Path) -> Optional[Solution]:
        """Return solution for the path if the final step exists.

        Args:
            path (Path): path to select solution for.

        Returns:
            Optional[Solution]: solution connected to the final step.
        """
        final_step = path.steps.filter(is_final=True).first()
        if final_step:
            return final_step.solution
        return None
