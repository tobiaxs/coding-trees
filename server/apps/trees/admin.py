"""Admin site config for the trees app."""
from django.contrib import admin

from server.apps.trees.models import Option, Path, Solution, Step, Tree

admin.site.register(Solution)
admin.site.register(Option)
admin.site.register(Step)
admin.site.register(Path)
admin.site.register(Tree)
