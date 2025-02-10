from django.contrib.auth.base_user import BaseUserManager
from django.db.models.query import QuerySet


class UserManager(BaseUserManager):
    """
    User Manager
    Inherit from Base User Manger for assign NonDeletedQuerySet as user queryset_class
    methods:
        - create_user: Create and save a user with the given phone_number, email, and password.
        - create_superuser: Create and save a Super User user with the given phone_number, email, and password.
        - get_restore_or_create: override to set queryset class
        - restore: override to set queryset class
        - get_queryset: override to set queryset class

    """

    qs_class = QuerySet
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given phone_number, email, and password.
        """
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)

    def get_restore_or_create(self, *args, **kwargs):
        return self.get_queryset().get_restore_or_create(*args, **kwargs)

    def restore(self, *args, **kwargs):
        return self.get_queryset().restore(*args, **kwargs)

    def get_queryset(self):
        return self.qs_class(self.model, using=self._db)
