from typing import Any

from unfold.forms import UserCreationForm


class NormalUserCreationForm(UserCreationForm):
    """
    A form for creating normal users.

    This form inherits from `UserCreationForm` and configures it for normal user creation.
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize the form with provided arguments.

        Args:
            *args: Positional arguments passed to the parent class.
            **kwargs: Keyword arguments passed to the parent class.
        """
        super(NormalUserCreationForm, self).__init__(*args, **kwargs)

    def save(self, commit: bool = True) -> Any:
        """
        Save the normal user instance, setting specific fields.

        Args:
            commit (bool): Whether to save the instance to the database.

        Returns:
            User: The saved normal user instance.
        """
        self.instance.is_staff = False  # Mark the instance as not staff.
        self.instance.is_superuser = False  # Mark the instance as not a superuser.
        return super().save(commit)  # Save the instance to the database.
