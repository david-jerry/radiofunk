from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = "radio_funk.users"
    verbose_name = _("Users")

    def ready(self):
        try:
            import radio_funk.users.signals  # noqa F401
        except ImportError:
            pass
