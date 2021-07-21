"""Admin site config for the users app."""
from django.contrib import admin

from server.apps.users.models import User

admin.site.register(User)
