from django.apps import AppConfig


class GenreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'radio_funk.genre'

    def ready(self):
        try:
            import radio_funk.genre.signals  # noqa F401
        except ImportError:
            pass
