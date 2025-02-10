from rest_framework.permissions import IsAuthenticated


class IsSuperUser(IsAuthenticated):
    """
    Permission class to allow access only to superusers.

    Inherits from `IsAuthenticated` to ensure that the user is authenticated.
    This class provides additional checks to verify if the user has superuser privileges.
    """

    def has_permission(self, request, view) -> bool:
        """
        Check if the request has permission based on the user's superuser status.

        Args:
            request: The HTTP request object.
            view: The view that is being accessed.

        Returns:
            bool: True if the user is a superuser, False otherwise.
        """
        return bool(request.user and request.user.is_superuser)

    def has_object_permission(self, request, view, obj) -> bool:
        """
        Check if the request has object-level permission based on the user's superuser status.

        Args:
            request: The HTTP request object.
            view: The view that is being accessed.
            obj: The object being accessed.

        Returns:
            bool: True if the user is a superuser, False otherwise.
        """
        return bool(request.user and request.user.is_superuser)
