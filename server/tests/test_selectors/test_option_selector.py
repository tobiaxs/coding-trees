"""Tests for option selector classes."""

import pytest

from server.apps.trees.selectors import OptionSelector
from server.tests.factories import OptionFactory, PathFactory, TreeFactory

pytestmark = [pytest.mark.django_db]


def test_options_for_step_name_and_tree(
    tree_factory: TreeFactory,
    option_factory: OptionFactory,
    path_factory: PathFactory,
):
    """Check if 'for_step_name_and_tree' returns correct options."""
    tree = tree_factory()
    for _ in range(3):
        path = path_factory()
        tree.paths.add(path)
        option_factory(step__name="Some Step", step__path=path)
        option_factory(step__name="Another Step", step__path=path)
    options = OptionSelector.for_step_name_and_tree("Some Step", tree)

    assert options.count() == 3
