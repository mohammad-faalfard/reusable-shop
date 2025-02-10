from datetime import timedelta

from django.http import HttpRequest
from django.utils import timezone

from ..models import NewUserProxy


def new_user_badge_callback(request: HttpRequest) -> int:
    """
    Counts new users who joined within the last 24 hours.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        int: Count of new users who joined within the last 24 hours.
    """
    start_time = (timezone.now() - timedelta(days=1)).date()
    return NewUserProxy.objects.filter(date_joined__date__gte=start_time).count()
