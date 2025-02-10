from typing import Any

from unfold.forms import UserCreationForm


class AdminUserCreationForm(UserCreationForm):
    """
    A form for creating admin users.

    This form inherits from `UserCreationForm` and adds specific fields and behaviors for admin users.
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize the form with provided arguments.

        Args:
            *args: Positional arguments passed to the parent class.
            **kwargs: Keyword arguments passed to the parent class.
        """
        super(AdminUserCreationForm, self).__init__(*args, **kwargs)

    def save(self, commit: bool = True) -> Any:
        """
        Save the admin user instance, setting specific fields.

        Args:
            commit (bool): Whether to save the instance to the database.

        Returns:
            User: The saved admin user instance.
        """
        self.instance.is_staff = True  # Mark the instance as staff.
        self.instance.is_superuser = True  # Mark the instance as a superuser.
        self.instance.is_verified = True  # Mark the instance as verified.
        self.instance.is_admin_verified = True  # Mark the instance as admin verified.
        return super().save(commit)  # Save the instance to the database.
