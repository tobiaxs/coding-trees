"""Tests for step selector classes."""

import pytest

from server.apps.trees.selectors import StepSelector
from server.tests.factories import TreeFactory
from server.tests.test_helpers import create_path_step_options_for_tree

pytestmark = [pytest.mark.django_db]


def test_first_step_name_for_tree(
    tree_factory: TreeFactory,
):
    """Check if the first step name is returned for given tree.

    Only one step name is present.
    """
    tree = tree_factory()
    for _ in range(3):
        create_path_step_options_for_tree("First Step", tree)
    step_name = StepSelector.first_name_for_tree(tree)

    assert step_name == "First Step"


def test_first_step_name_for_tree_many_steps(
    tree_factory: TreeFactory,
):
    """Check if the first step name is returned for given tree.

    Two step names are present. Steps majority has the most options.
    3 steps with 3 options combined and 1 step with 1 option.
    """
    tree = tree_factory()
    for _ in range(3):
        create_path_step_options_for_tree("First Step", tree)
    create_path_step_options_for_tree("Another First Step", tree)
    step_name = StepSelector.first_name_for_tree(tree)

    assert step_name == "First Step"


def test_first_step_name_for_tree_less_steps(
    tree_factory: TreeFactory,
):
    """Check if the first step name is returned for given tree.

    Two step names are present. Steps minority has the most options.
    3 steps with 3 options combined and 1 step with 4 options.
    """
    tree = tree_factory()
    for _ in range(3):
        create_path_step_options_for_tree("First Step", tree)
    create_path_step_options_for_tree("Another First Step", tree, 4)
    step_name = StepSelector.first_name_for_tree(tree)

    assert step_name == "Another First Step"
