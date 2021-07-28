"""Tests for solution model API."""

import pytest
from django.urls import reverse
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED
from rest_framework.test import APIClient

from server.apps.trees.models import Solution
from server.tests.conftest import SolutionFactory

pytestmark = [pytest.mark.django_db]


def test_solution_create_api(api_client: APIClient):
    """Test creating solution instance using solution api."""
    response = api_client.post(
        reverse("trees:solutions-list"),
        data={"name": "Test Solution", "description": "Test Description"},
    )

    assert response.status_code == HTTP_201_CREATED
    assert Solution.objects.count() == 1


def test_solution_update_api(
    api_client: APIClient,
    solution_factory: SolutionFactory,
):
    """Test updating solution instance using solution api."""
    solution = solution_factory()

    response = api_client.put(
        reverse("trees:solutions-detail", kwargs={"pk": solution.pk}),
        data={
            "name": "Test Solution Updated",
            "description": "Test Description Updated",
        },
    )
    solution.refresh_from_db()

    assert response.status_code == HTTP_200_OK
    assert Solution.objects.count() == 1
    assert solution.name == "Test Solution Updated"
    assert solution.description == "Test Description Updated"
