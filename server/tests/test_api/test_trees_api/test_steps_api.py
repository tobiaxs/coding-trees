"""Tests for steps model API."""

import pytest
from django.urls import reverse
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
)
from rest_framework.test import APIClient

from server.apps.trees.models import Step
from server.tests.factories import (
    OptionFactory,
    PathFactory,
    SolutionFactory,
    StepFactory,
)

pytestmark = [pytest.mark.django_db]


def test_step_create_api(api_client: APIClient, path_factory: PathFactory):
    """Test creating step instance using step api."""
    path = path_factory()
    response = api_client.post(
        reverse("trees:steps-list"),
        data={"name": "Test Step", "path": path.pk},
    )
    created_step = Step.objects.get(name="Test Step")

    assert response.status_code == HTTP_201_CREATED
    assert created_step
    assert created_step.path == path


def test_step_create_api_with_options(
    api_client: APIClient,
    path_factory: PathFactory,
    option_factory: OptionFactory,
):
    """Test creating step instance using step api.

    Preceding options are passed to the step.
    """
    preceding_options = [option.pk for option in option_factory.create_batch(3)]
    response = api_client.post(
        reverse("trees:steps-list"),
        data={
            "name": "Test Step",
            "path": path_factory().pk,
            "preceding_options": preceding_options,
        },
    )
    created_step = Step.objects.get(name="Test Step")

    assert response.status_code == HTTP_201_CREATED
    assert created_step
    assert (
        list(created_step.preceding_options.all().values_list("pk", flat=True))
        == preceding_options
    )


def test_step_create_api_with_solution(
    api_client: APIClient,
    path_factory: PathFactory,
    solution_factory: SolutionFactory,
):
    """Test creating step instance using step api.

    Solution is passed to the step and 'is_final' is set to True.
    """
    solution = solution_factory()
    response = api_client.post(
        reverse("trees:steps-list"),
        data={
            "name": "Test Step",
            "path": path_factory().pk,
            "solution": solution.pk,
            "is_final": True,
        },
    )
    created_step = Step.objects.get(name="Test Step")

    assert response.status_code == HTTP_201_CREATED
    assert created_step
    assert created_step.solution == solution


def test_step_create_api_first_and_final(
    api_client: APIClient,
    path_factory: PathFactory,
):
    """Test creating step instance using step api.

    Both 'is_first' and 'is_final' are set to True.
    """
    response = api_client.post(
        reverse("trees:steps-list"),
        data={
            "name": "Test Step",
            "path": path_factory().pk,
            "is_first": True,
            "is_final": True,
        },
    )

    assert response.status_code == HTTP_400_BAD_REQUEST
    assert response.data["non_field_errors"] == [
        "A step cannot be both first and final.",
    ]


def test_step_create_api_final_no_solution(
    api_client: APIClient,
    path_factory: PathFactory,
):
    """Test creating step instance using step api.

    'is_final' is set to True, but no solution is passed.
    """
    response = api_client.post(
        reverse("trees:steps-list"),
        data={
            "name": "Test Step",
            "path": path_factory().pk,
            "is_final": True,
        },
    )

    assert response.status_code == HTTP_400_BAD_REQUEST
    assert response.data["non_field_errors"] == [
        "A solution can only be (and has to be) set on the final step.",
    ]


def test_step_update_api(api_client: APIClient, step_factory: StepFactory):
    """Test updating step instance using step api."""
    step = step_factory()
    response = api_client.put(
        reverse("trees:steps-detail", kwargs={"pk": step.pk}),
        data={"name": "Test Step Updated"},
    )
    step.refresh_from_db()

    assert response.status_code == HTTP_200_OK
    assert step.name == "Test Step Updated"
