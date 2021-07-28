from django.apps import AppConfig


class TreesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "server.apps.trees"

    def ready(self):
        """Connect trees app signals."""
        import server.apps.trees.signals
