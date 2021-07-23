"""Test for tree app models."""
import pytest
from django.db.utils import IntegrityError

from server.tests.conftest import (
    OptionFactory,
    PathFactory,
    SolutionFactory,
    StepFactory,
    TreeFactory,
)

pytestmark = [pytest.mark.django_db]


# Str methods


def test_tree_str(tree_factory: TreeFactory):
    """Check str method for tree model."""
    tree = tree_factory()
    assert str(tree) == tree.name


def test_path_str(path_factory: PathFactory):
    """Check str method for path model."""
    path = path_factory()
    assert str(path) == path.name


def test_step_str(step_factory: StepFactory):
    """Check str method for step model."""
    step = step_factory()
    assert str(step) == step.name


def test_option_str(option_factory: OptionFactory):
    """Check str method for option model."""
    option = option_factory()
    assert str(option) == option.name


def test_solution_str(solution_factory: SolutionFactory):
    """Check str method for solution model."""
    solution = solution_factory()
    assert str(solution) == solution.name


# Constraints


def test_not_first_and_final_constraint(step_factory: StepFactory):
    """Check if integrity error is raised.

    'is_first' and 'is_final' are both set to true.
    """
    step = step_factory()
    step.is_first = True
    step.is_final = True
    with pytest.raises(IntegrityError):
        step.save()


def test_not_final_with_no_solution_constraint(step_factory: StepFactory):
    """Check if integrity error is raised.

    'is_final' is set to true and no 'solution' is set.
    """
    step = step_factory()
    step.is_final = True
    with pytest.raises(IntegrityError):
        step.save()


def test_steps_not_equal_constraint(
    step_factory: StepFactory,
    option_factory: OptionFactory,
):
    """Check if integrity error is raised when steps are equal."""
    step = step_factory()
    option = option_factory(step=step)
    option.next_step = step
    with pytest.raises(IntegrityError):
        option.save()


# Properties


def test_path_solution_property(
    path_factory: PathFactory,
    step_factory: StepFactory,
    solution_factory: SolutionFactory,
):
    """Check if solution property returns solution from the final step."""
    path = path_factory()
    steps = [
        step_factory(is_first=True),
        step_factory(is_final=True, solution=solution_factory()),
    ]
    path.steps.set(steps)
    assert path.solution == steps[-1].solution


def test_path_no_solution_property(path_factory: PathFactory):
    """Check if solution property returns None when there is no final step."""
    path = path_factory()
    assert path.solution is None
