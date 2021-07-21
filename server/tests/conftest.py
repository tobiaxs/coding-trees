"""Common test fixtures."""
import pytest
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from server.apps.users.models import User

TEST_USER_CREDENTIALS = frozenset(
    {
        "username": "test_user",
        "email": "test@user.com",
        "password": "test-password",
    }.items(),
)


@pytest.fixture
def api_client() -> APIClient:
    """Prepare an API client with authenticated user.

    Returns:
        APIClient: A configured API client.
    """
    user = User.objects.create_user(**dict(TEST_USER_CREDENTIALS))
    client = APIClient()
    refresh = RefreshToken.for_user(user)
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")

    return client
