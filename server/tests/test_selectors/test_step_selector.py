"""Tests for step selector classes."""

import pytest

from server.apps.trees.selectors import StepSelector
from server.tests.conftest import (
    OptionFactory,
    PathFactory,
    StepFactory,
    TreeFactory,
)

pytestmark = [pytest.mark.django_db]


def test_first_step_for_tree(
    tree_factory: TreeFactory,
    path_factory: PathFactory,
    step_factory: StepFactory,
):
    """Check if the first step is returned for given tree.

    Only one 'is_first' is present.
    """
    tree = tree_factory()
    path = path_factory()
    steps = [step_factory() for _ in range(3)]

    tree.paths.add(path)
    path.steps.set(steps)
    steps[0].is_first = True
    steps[0].save()

    assert StepSelector.first_for_tree(tree) == steps[0]


def test_multiple_first_steps_for_tree(
    tree_factory: TreeFactory,
    path_factory: PathFactory,
    step_factory: StepFactory,
    option_factory: OptionFactory,
):
    """Check if the first step is returned for given tree.

    Multiple 'is_first' are present,
    the one with the most options should be returned.
    """
    tree = tree_factory()
    paths = [path_factory() for _ in range(3)]
    steps = [step_factory(is_first=True) for _ in range(3)]

    for index, step in enumerate(steps):
        path = paths[index]
        path.steps.add(step)
        step.options.set([option_factory() for _ in range(index)])

    tree.paths.set(paths)

    assert StepSelector.first_for_tree(tree) == steps[-1]
