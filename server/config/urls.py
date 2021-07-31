"""URLs config for the server project."""

from django.contrib import admin
from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import include, path
from django.views.generic.base import RedirectView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

# Default URL routes.
urlpatterns = [
    path("", RedirectView.as_view(url="admin/")),
    path("admin/", admin.site.urls),
    path("api/", include("rest_framework.urls")),
    path(
        "favicon.ico",
        RedirectView.as_view(url=staticfiles_storage.url("favicon.ico")),
    ),
]

# Swagger URL routes.
urlpatterns += [
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(), name="docs"),
]

# Apps URL routes.
urlpatterns += [
    path(
        "api/users/",
        include("server.apps.users.api.urls", namespace="users"),
    ),
    path(
        "api/trees/",
        include("server.apps.trees.api.urls", namespace="trees"),
    ),
]
