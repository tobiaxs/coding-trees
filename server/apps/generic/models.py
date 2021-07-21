"""Generic app models."""
import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


class GenericModel(models.Model):
    """Base model for storing fields necessary for every model."""

    uuid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)

    class Meta:
        abstract = True
