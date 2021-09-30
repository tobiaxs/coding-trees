"""Factories for app models."""

import factory
from factory import fuzzy  # noqa: WPS458
from pytest_factoryboy import register

from server.apps.trees.models import Option, Path, Solution, Step, Tree
from server.apps.users.models import User

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
    description = fuzzy.FuzzyText(length=30)
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
    path = factory.SubFactory(PathFactory)

    class Meta:
        model = Step


class OptionFactory(factory.django.DjangoModelFactory):
    """Factory for option model."""

    name = fuzzy.FuzzyText(length=10)
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
