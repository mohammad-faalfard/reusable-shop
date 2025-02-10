from django.http import HttpRequest

from .queries import get_notifications


def total_notifications(request: HttpRequest) -> int:
    if request.user.is_anonymous:
        return {"total_notifs": 0}
    total_notifs: int = get_notifications(user=request.user).filter(is_seen=False).count()
    return {"total_notifs": total_notifs}
