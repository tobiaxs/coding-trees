"""URLs config for the server project."""
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

# Default URL routes.
urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("rest_framework.urls")),
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
]
