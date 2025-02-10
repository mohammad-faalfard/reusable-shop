from django.db import models


class DefaultManager(models.Manager):
    """
    Custom manager for filtering active and inactive records.
    """

    def get_queryset(self):
        """Returns the default queryset."""
        return super().get_queryset()

    def active(self):
        """Return only active records (is_active=True)."""
        return self.get_queryset().filter(is_active=True)

    def inactive(self):
        """Return only inactive records (is_active=False)."""
        return self.get_queryset().filter(is_active=False)
