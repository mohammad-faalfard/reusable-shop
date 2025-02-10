from apps.account.models import User

from .models import UserMessage


def get_notification(user: User, user_message_id: int) -> UserMessage:
    return UserMessage.objects.filter(is_active=True, pk=user_message_id, user=user, send_in_app=True).first()


def get_notifications(user: User) -> list[UserMessage]:
    return UserMessage.objects.filter(is_active=True, user=user, send_in_app=True)


def seen_user_message(user_message: UserMessage) -> UserMessage:
    user_message.is_seen = True
    user_message.save()
    return user_message
