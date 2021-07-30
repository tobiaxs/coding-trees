"""Helper functions and classes for app tests."""


from server.apps.trees.models import Tree
from server.tests.factories import OptionFactory, StepFactory


def create_path_step_options_for_tree(
    step_name: str,
    tree: Tree,
    options_no: int = 1,
    next_step: bool = False,
) -> None:
    """Create a path, step with given name and given number of options.

    Args:
        step_name (str): name of the step.
        tree (Tree): tree for which the path is created.
        options_no (int): number of options to create. Defaults to 1.
        next_step (bool): indicates if the option should have the next step.
            Defaults to False.
    """
    step = StepFactory(name=step_name, is_first=True)
    option_next_step = (
        StepFactory(name="Second Step", is_first=False) if next_step else None
    )
    OptionFactory.create_batch(
        options_no,
        step=step,
        next_step=option_next_step,
    )
    tree.paths.add(step.path)
