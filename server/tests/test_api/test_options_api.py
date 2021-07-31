"""Tests for option model API."""

import pytest
from django.urls import reverse
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
)
from rest_framework.test import APIClient

from server.apps.trees.models import Option
from server.tests.factories import OptionFactory, StepFactory

pytestmark = [pytest.mark.django_db]


def test_option_create_api(api_client: APIClient, step_factory: StepFactory):
    """Test creating option instance using options api."""
    step = step_factory()
    response = api_client.post(
        reverse("trees:options-list"),
        data={"name": "Test Option", "step": step.pk},
    )
    created_option = Option.objects.get(name="Test Option")

    assert response.status_code == HTTP_201_CREATED
    assert created_option
    assert created_option.step == step


def test_option_create_api_with_both_steps(
    api_client: APIClient,
    step_factory: StepFactory,
):
    """Test creating option instance using options api.

    Both steps should be present.
    """
    step = step_factory()
    next_step = step_factory()
    response = api_client.post(
        reverse("trees:options-list"),
        data={
            "name": "Test Option",
            "step": step.pk,
            "next_step": next_step.pk,
        },
    )
    created_option = Option.objects.get(name="Test Option")

    assert response.status_code == HTTP_201_CREATED
    assert created_option
    assert created_option.step == step


def test_option_create_api_same_steps(
    api_client: APIClient,
    step_factory: StepFactory,
):
    """Test creating option instance using options api.

    Both steps are the same.
    """
    step = step_factory()
    response = api_client.post(
        reverse("trees:options-list"),
        data={"name": "Test Option", "step": step.pk, "next_step": step.pk},
    )

    assert response.status_code == HTTP_400_BAD_REQUEST
    assert response.data["non_field_errors"] == [
        "A step cannot be the same as the next step.",
    ]


def test_option_update_api(
    api_client: APIClient,
    step_factory: StepFactory,
    option_factory: OptionFactory,
):
    """Test updating option instance using options api."""
    option = option_factory(next_step=step_factory())
    new_step = step_factory()

    response = api_client.put(
        reverse("trees:options-detail", kwargs={"pk": option.pk}),
        data={"name": "Test Option Updated", "step": new_step.pk},
    )
    option.refresh_from_db()

    assert response.status_code == HTTP_200_OK
    assert option.name == "Test Option Updated"
    assert option.step == new_step


def test_option_update_api_with_both_steps(
    api_client: APIClient,
    step_factory: StepFactory,
    option_factory: OptionFactory,
):
    """Test updating option instance using options api.

    Both steps should be updated.
    """
    option = option_factory()
    new_step = step_factory()
    new_next_step = step_factory()

    response = api_client.put(
        reverse("trees:options-detail", kwargs={"pk": option.pk}),
        data={
            "name": "Test Option Updated",
            "step": new_step.pk,
            "next_step": new_next_step.pk,
        },
    )
    option.refresh_from_db()

    assert response.status_code == HTTP_200_OK
    assert option.name == "Test Option Updated"
    assert option.step == new_step
    assert option.next_step == new_next_step
