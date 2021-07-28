"""Signals for the trees app models."""

from django.db.models import Count
from django.db.models.signals import pre_delete
from django.dispatch import receiver

from server.apps.trees.models import Path, Step


@receiver(pre_delete, sender=Path, dispatch_uid="pre_delete_path")
def pre_delete_path(sender: type[Path], instance: Path, **kwargs) -> None:
    """Delete the steps that were only connected to this path.

    Args:
        sender (type[Path]): Path class.
        instance (Path): Path instance.
        kwargs: Keyword arguments.
    """
    Step.objects.annotate(paths_count=Count("paths")).filter(
        paths=instance,
        paths_count=1,
    ).delete()
