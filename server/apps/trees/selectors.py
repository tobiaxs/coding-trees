"""Selector classes for tree app models."""

from typing import Optional

from django.db.models import Count

from server.apps.trees.models import Path, Solution, Step, Tree


class StepSelector:
    """Handle step fetching operations."""

    @classmethod
    def first_for_tree(cls, tree: Tree) -> Optional[Step]:
        """Return the first step for the tree.

        If multiple first steps are found, return the one with the most options.

        Args:
            tree (Tree): given tree.

        Returns:
            Optional[Step]: first step for the tree.
        """
        steps = Step.objects.filter(paths__trees=tree, is_first=True)
        if steps.count() > 1:
            return (
                steps.annotate(options_count=Count("options"))
                .order_by("-options_count")
                .first()
            )
        return steps.first()


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
