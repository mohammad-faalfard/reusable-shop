from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

from .notification import send_notification
from .sms import send_simple_sms


@shared_task
def create_child_messages_for_group(message_id: int):
    from .models import GroupMessage, GroupUser, UserMessage

    group_message = GroupMessage.objects.get(id=message_id)
    users = GroupUser.objects.filter(group=group_message.group).values_list("user_id", flat=True)
    for user_id in users:
        UserMessage.objects.create(
            user_id=user_id,
            title=group_message.title,
            content=group_message.content,
            send_in_app=group_message.send_in_app,
            send_notification=group_message.send_notification,
            send_email=group_message.send_email,
            send_sms=group_message.send_sms,
        )


@shared_task
def send_simple_sms_task(receptor: str, message: str):
    send_simple_sms(receptor=receptor, message=message)


@shared_task
def send_email_task(receiver: str, subject: str, content: str):
    send_mail(
        subject,
        content,
        settings.EMAIL_HOST_USER,
        [receiver],
        fail_silently=True,
    )


@shared_task
def send_notification_task(user_id: int, title: str, content: str, event_type: int, event_data: str) -> None:
    from .models import UserDevice

    receiver: list[str] = [str(uuid) for uuid in UserDevice.objects.filter(user=user_id).values_list("token", flat=True)]
    # Front-End Url that user click on this push notif be redirected
    url: str = ""
    send_notification(receiver, title, content, url)
