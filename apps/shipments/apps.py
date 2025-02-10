from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ShipmentsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.shipments"
    verbose_name = _("Shipments Management")
