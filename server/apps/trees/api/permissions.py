"""Permission classes for the trees API."""

from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.views import APIView

READONLY_ALLOWED_METHODS = ("GET", "OPTIONS")


class IsSuperuserOrReadOnly(BasePermission):
    """Used for crud-access for the superusers.

    Fallbacks to read-only for non superuser.
    """

    def has_permission(self, request: Request, view: APIView) -> bool:
        """Return True if user is superuser or request is read-only.

        Args:
            request (Request): incoming request.
            view (APIView): view using the permission.

        Returns:
            bool: has permission or not.
        """
        return request.method in READONLY_ALLOWED_METHODS or (
            request.user and request.user.is_superuser
        )
