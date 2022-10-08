from django.apps import AppConfig


class MyStoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "my_store"

    def ready(self):
        import my_store.signals.handlers
