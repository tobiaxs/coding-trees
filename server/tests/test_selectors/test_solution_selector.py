"""Tests for solution selector classes."""

import pytest

from server.apps.trees.selectors import SolutionSelector
from server.tests.factories import PathFactory, SolutionFactory, StepFactory

pytestmark = [pytest.mark.django_db]


def test_path_solution_for_path(
    path_factory: PathFactory,
    step_factory: StepFactory,
    solution_factory: SolutionFactory,
):
    """Check if Solution for_path returns Solution from the final Step."""
    path = path_factory()
    steps = [
        step_factory(is_first=True),
        step_factory(is_final=True, solution=solution_factory()),
    ]
    path.steps.set(steps)

    assert SolutionSelector.for_path(path) == steps[-1].solution


def test_path_no_solution_for_path(path_factory: PathFactory):
    """Check if Solution for_path returns None when there is no final Step."""
    path = path_factory()
    assert SolutionSelector.for_path(path) is None
