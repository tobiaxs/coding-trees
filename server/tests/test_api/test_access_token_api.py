"""Feel free to delete this file, as it's only to trigger pytest initialy."""

import pytest
from django.urls import reverse
from rest_framework.status import HTTP_200_OK
from rest_framework.test import APIClient

from server.tests.conftest import TEST_USER_CREDENTIALS


@pytest.mark.django_db
def test_access_token_api(api_client: APIClient):
    """Tests the refresh_token API endpoint."""
    response = api_client.post(
        reverse("users:token_obtain"),
        data=dict(TEST_USER_CREDENTIALS),
    )
    assert response.status_code == HTTP_200_OK
    assert response.data["access"]
    assert response.data["refresh"]
