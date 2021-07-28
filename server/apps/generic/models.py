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

    def save(self, *args, **kwargs) -> None:
        """Call full_clean() before saving.

        Args:
            args(list): save arguments.
            kwargs(dict): save keyword arguments.
        """
        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        abstract = True


class GenericModelWithCreator(GenericModel):
    """Abstract model for models that require a creator."""

    creator = models.ForeignKey("users.User", on_delete=models.CASCADE)

    class Meta:
        abstract = True
