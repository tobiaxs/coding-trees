"""Common test fixtures and factories."""
import factory
import pytest
from factory import fuzzy  # noqa: WPS458
from pytest_factoryboy import register
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from server.apps.trees.models import Option, Path, Solution, Step, Tree
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
    user = User.objects.create_user(
        **dict(TEST_USER_CREDENTIALS),
        is_superuser=True,
    )
    client = APIClient()
    refresh = RefreshToken.for_user(user)
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")

    return client


# Users factories


class UserFactory(factory.django.DjangoModelFactory):
    """Factory for user model."""

    username = fuzzy.FuzzyText(length=10)
    email = fuzzy.FuzzyText(length=10, suffix="@email.com")
    password = fuzzy.FuzzyText(length=10)

    class Meta:
        model = User


register(UserFactory)


# Trees factories


class TreeFactory(factory.django.DjangoModelFactory):
    """Factory for tree model."""

    name = fuzzy.FuzzyText(length=10)
    creator = factory.SubFactory(UserFactory)

    class Meta:
        model = Tree


class PathFactory(factory.django.DjangoModelFactory):
    """Factory for path model."""

    name = fuzzy.FuzzyText(length=10)
    creator = factory.SubFactory(UserFactory)

    class Meta:
        model = Path


class StepFactory(factory.django.DjangoModelFactory):
    """Factory for step model."""

    name = fuzzy.FuzzyText(length=10)
    creator = factory.SubFactory(UserFactory)
    path = factory.SubFactory(PathFactory)

    class Meta:
        model = Step


class OptionFactory(factory.django.DjangoModelFactory):
    """Factory for option model."""

    name = fuzzy.FuzzyText(length=10)
    creator = factory.SubFactory(UserFactory)
    step = factory.SubFactory(StepFactory)

    class Meta:
        model = Option


class SolutionFactory(factory.django.DjangoModelFactory):
    """Factory for solution model."""

    name = fuzzy.FuzzyText(length=10)
    creator = factory.SubFactory(UserFactory)
    description = fuzzy.FuzzyText(length=10)

    class Meta:
        model = Solution


register(TreeFactory)
register(PathFactory)
register(StepFactory)
register(OptionFactory)
register(SolutionFactory)
