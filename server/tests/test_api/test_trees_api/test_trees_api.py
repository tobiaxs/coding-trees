"""Tests for tree model API."""

import pytest
from django.urls import reverse
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED
from rest_framework.test import APIClient

from server.apps.trees.models import Tree
from server.tests.factories import TreeFactory

pytestmark = [pytest.mark.django_db]


def test_tree_create_api(api_client: APIClient):
    """Test creating tree instance using trees api."""
    response = api_client.post(
        reverse("trees:trees-list"),
        data={"name": "Test Tree"},
    )

    assert response.status_code == HTTP_201_CREATED
    assert Tree.objects.count() == 1


def test_tree_update_api(api_client: APIClient, tree_factory: TreeFactory):
    """Test updating tree instance using trees api."""
    tree = tree_factory()
    response = api_client.put(
        reverse("trees:trees-detail", kwargs={"pk": tree.pk}),
        data={"name": "New Name"},
    )
    tree.refresh_from_db()

    assert response.status_code == HTTP_200_OK
    assert tree.name == "New Name"
