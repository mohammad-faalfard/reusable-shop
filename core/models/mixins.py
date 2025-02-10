from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_lifecycle import BEFORE_CREATE, BEFORE_UPDATE, hook

from core.middleware.thread_local_middleware import get_current_user


class UpdatedByMixin(models.Model):
    """
    Mixin to automatically set the `updated_by` field to the current user
    before an update. Requires middleware that sets the user in thread-local storage.
    """

    updated_by = models.ForeignKey(
        "account.User",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="%(class)s_updated_by",  # Unique related_name using model name
        verbose_name=_("Updated by"),
    )

    @hook(BEFORE_UPDATE)
    def set_updated_by_user(self):
        """
        Hook to set the `updated_by` field with the current user, if available.
        Uses the get_current_user function to retrieve the user from thread-local storage.
        """
        current_user = get_current_user()

        if current_user:
            self.updated_by = current_user

    class Meta:
        abstract = True


class CreatedByMixin(models.Model):
    """
    Mixin to automatically set the `created_by` field to the current user
    on creation. Requires middleware that sets the user in thread-local storage.
    """

    created_by = models.ForeignKey(
        "account.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(class)s_created_by",  # Unique related_name using model name
        verbose_name=_("Created By"),
    )

    @hook(BEFORE_CREATE)
    def set_created_by_user(self):
        """
        Hook to set the `created_by` field with the current user on creation, if available.
        Uses the `get_current_user` function to retrieve the user from thread-local storage.
        """
        current_user = get_current_user()
        if current_user and not self.created_by:
            self.created_by = current_user

    class Meta:
        abstract = True


class PriorityMixin(models.Model):
    """
    Mixin to add a `priority` field to a model.
    The priority is a small integer with a minimum value of 0.
    """

    priority = models.PositiveSmallIntegerField(
        verbose_name=_("Priority"),
        validators=[
            MinValueValidator(0),  # Start priority from 0
        ],
        default=0,  # Set default priority to 0
        help_text=_("Priority of the record. Starting from 0"),
        db_index=True,
    )

    class Meta:
        abstract = True


# class IsActiveMixin(models.Model):
#     """
#     Mixin that adds an `is_active` field to a model.
#     """

#     is_active = models.BooleanField(
#         verbose_name=_("Is active"),
#         default=True,
#         db_index=True,
#         help_text=_("Indicates if the instance is active."),
#     )

#     class Meta:
#         abstract = True
