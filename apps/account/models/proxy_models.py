# apps/account/models/proxy_models.py

from django.utils.translation import gettext_lazy as _

from .user import User


class AdminUserProxy(User):
    """
    Proxy model for admin users.

    Meta:
        proxy (bool): Set to True to avoid creating a new database table.
        verbose_name (str): Custom name for display in Django admin.
        verbose_name_plural (str): Plural name for display in Django admin.
    """

    class Meta:
        proxy = True
        verbose_name = _("admin user")
        verbose_name_plural = _("admin users")


class NormalUserProxy(User):
    """
    Proxy model for regular users.

    Meta:
        proxy (bool): Set to True to avoid creating a new database table.
        verbose_name (str): Custom name for display in Django admin.
        verbose_name_plural (str): Plural name for display in Django admin.
    """

    class Meta:
        proxy = True
        verbose_name = _("Normal user")
        verbose_name_plural = _("Normal users")


class NewUserProxy(User):
    """
    Proxy model for new users.

    Meta:
        proxy (bool): Set to True to avoid creating a new database table.
        verbose_name (str): Custom name for display in Django admin.
        verbose_name_plural (str): Plural name for display in Django admin.
    """

    class Meta:
        proxy = True
        verbose_name = _("new user")
        verbose_name_plural = _("new users")
