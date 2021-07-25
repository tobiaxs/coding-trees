"""URLs config for the trees app."""
from django.urls import include, path
from rest_framework import routers

from server.apps.trees.api.views.option import OptionViewSet
from server.apps.trees.api.views.path import PathViewSet
from server.apps.trees.api.views.solution import SolutionViewSet
from server.apps.trees.api.views.step import StepViewSet
from server.apps.trees.api.views.tree import TreeViewSet

app_name = "trees"

router = routers.DefaultRouter()

router.register("solutions", SolutionViewSet, basename="solutions")
router.register("options", OptionViewSet, basename="options")
router.register("steps", StepViewSet, basename="steps")
router.register("paths", PathViewSet, basename="paths")
router.register("", TreeViewSet, basename="trees")

urlpatterns = [
    path("", include(router.urls)),
]
