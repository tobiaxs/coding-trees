"""Tests for decision tree api."""

import pytest
from django.urls import reverse
from rest_framework.status import HTTP_200_OK
from rest_framework.test import APIClient

from server.apps.trees.models import Option, Step
from server.tests.factories import OptionFactory, SolutionFactory, TreeFactory
from server.tests.test_helpers import create_path_step_options_for_tree

pytestmark = [pytest.mark.django_db]


def test_tree_first_step_no_data(
    api_client: APIClient,
    tree_factory: TreeFactory,
):
    """Test retrieving first step data for the tree.

    No steps are available.
    """
    tree = tree_factory()
    response = api_client.get(
        reverse("trees:trees-first-step", kwargs={"pk": tree.pk}),
    )

    assert response.status_code == HTTP_200_OK
    assert not response.data


def test_tree_first_step(
    api_client: APIClient,
    tree_factory: TreeFactory,
):
    """Test retrieving first step data for the tree.

    Simplest case when there is only one first step and no next ones.
    """
    tree = tree_factory()
    for _ in range(3):
        create_path_step_options_for_tree("First Step", tree)
    response = api_client.get(
        reverse("trees:trees-first-step", kwargs={"pk": tree.pk}),
    )

    assert response.status_code == HTTP_200_OK
    assert response.data["name"] == "First Step"
    assert len(response.data["options"]) == 3


def test_tree_first_step_many_steps(
    api_client: APIClient,
    tree_factory: TreeFactory,
):
    """Test retrieving first step data for the tree.

    More complicated case when there are 2 different first steps,
    but still no next ones.
    """
    tree = tree_factory()
    for _ in range(3):
        create_path_step_options_for_tree("First Step", tree)
        create_path_step_options_for_tree("Another First Step", tree, 2)
    response = api_client.get(
        reverse("trees:trees-first-step", kwargs={"pk": tree.pk}),
    )

    assert response.status_code == HTTP_200_OK
    assert response.data["name"] == "Another First Step"
    assert len(response.data["options"]) == 6


def test_tree_first_step_with_next_steps(
    api_client: APIClient,
    tree_factory: TreeFactory,
):
    """Test retrieving first step data for the tree.

    Only one first step, but options are having the next steps.
    """
    tree = tree_factory()
    for _ in range(3):
        create_path_step_options_for_tree("First Step", tree, next_step=True)

    response = api_client.get(
        reverse("trees:trees-first-step", kwargs={"pk": tree.pk}),
    )
    assert response.status_code == HTTP_200_OK
    assert response.data["name"] == "First Step"
    assert len(response.data["options"]) == 3
    for option in response.data["options"]:
        assert Step.objects.filter(pk=option["next_step"]).exists() is True


def test_tree_next_step(
    api_client: APIClient,
    tree_factory: TreeFactory,
):
    """Test retrieving next step data for the tree."""
    tree = tree_factory()
    create_path_step_options_for_tree("First Step", tree, next_step=True)
    step = Step.objects.get(name="Second Step")
    response = api_client.post(
        reverse(
            "trees:trees-next-step",
            kwargs={"pk": tree.pk},
        ),
        data={"step": step.pk},
    )

    assert response.status_code == HTTP_200_OK
    assert response.data["name"] == "Second Step"
    assert not response.data["options"]


def test_tree_next_step_with_options(
    api_client: APIClient,
    tree_factory: TreeFactory,
    option_factory: OptionFactory,
):
    """Test retrieving next step data with options for the tree."""
    tree = tree_factory()
    for _ in range(3):
        create_path_step_options_for_tree("First Step", tree, next_step=True)
    steps = Step.objects.filter(name="Second Step")
    for step in steps:
        option_factory(step=step)
    response = api_client.post(
        reverse(
            "trees:trees-next-step",
            kwargs={"pk": tree.pk},
        ),
        data={"step": steps.last().pk},
    )

    assert response.status_code == HTTP_200_OK
    assert response.data["name"] == "Second Step"
    assert len(response.data["options"]) == 3


def test_tree_next_step_with_solution(
    api_client: APIClient,
    tree_factory: TreeFactory,
    solution_factory: SolutionFactory,
):
    """Test retrieving next step data with solution for the tree."""
    tree = tree_factory()
    for _ in range(3):
        create_path_step_options_for_tree("First Step", tree, next_step=True)
    step = Step.objects.filter(name="Second Step").last()
    step.is_final = True
    step.solution = solution_factory()
    step.save()

    response = api_client.post(
        reverse(
            "trees:trees-next-step",
            kwargs={"pk": tree.pk},
        ),
        data={"step": step.pk},
    )

    assert response.status_code == HTTP_200_OK
    assert response.data["name"] == "Second Step"
    assert response.data["solution"]["pk"] == str(step.solution.pk)


def test_tree_first_step_same_options(
    api_client: APIClient,
    tree_factory: TreeFactory,
):
    """Test retrieving first step data for the tree.

    Only one first step, but options are the same.
    """
    tree = tree_factory()
    for _ in range(3):
        create_path_step_options_for_tree("First Step", tree)
    Option.objects.all().update(name="All the same name")
    response = api_client.get(
        reverse("trees:trees-first-step", kwargs={"pk": tree.pk}),
    )

    assert response.status_code == HTTP_200_OK
    assert response.data["name"] == "First Step"
    assert len(response.data["options"]) == 1
