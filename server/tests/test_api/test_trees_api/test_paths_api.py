"""Tests for paths model API."""

import pytest
from django.urls import reverse
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
)
from rest_framework.test import APIClient

from server.apps.trees.models import Path, Step
from server.tests.conftest import PathFactory, StepFactory

pytestmark = [pytest.mark.django_db]


def test_path_create_api(api_client: APIClient):
    """Test creating path instance using path api."""
    response = api_client.post(
        reverse("trees:paths-list"),
        data={"name": "Test Path"},
    )

    assert response.status_code == HTTP_201_CREATED
    assert Path.objects.count() == 1


def test_path_update_api(api_client: APIClient, path_factory: PathFactory):
    """Test updating path instance using path api."""
    path = path_factory()
    response = api_client.put(
        reverse("trees:paths-detail", kwargs={"pk": path.pk}),
        data={"name": "Test Path Updated"},
    )
    path.refresh_from_db()

    assert response.status_code == HTTP_200_OK
    assert path.name == "Test Path Updated"


def test_path_delete_api(
    api_client: APIClient,
    path_factory: PathFactory,
    step_factory: StepFactory,
):
    """Test deleting path instance and connected steps using path api."""
    path = path_factory()
    step_factory.create_batch(3, path=path)
    response = api_client.delete(
        reverse("trees:paths-detail", kwargs={"pk": path.pk}),
    )

    assert response.status_code == HTTP_204_NO_CONTENT
    assert Path.objects.count() == 0
    assert Step.objects.count() == 0
