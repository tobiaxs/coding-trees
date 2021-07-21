"""User app models."""
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from server.apps.generic.models import GenericModel


class User(AbstractUser, GenericModel):
    """Wrapper around abstract User model."""

    email = models.EmailField(_("Email Address"), unique=True)
