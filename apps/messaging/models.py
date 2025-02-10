from django.db import models
from django.utils.translation import gettext_lazy as _
from django_lifecycle import AFTER_CREATE, hook

from core import choice
from core.models import BaseModel

from .tasks import create_child_messages_for_group, send_email_task, send_notification_task, send_simple_sms_task

# Pre-Compute for lookups
MESSAGE_EVENT_KEYS: set[int] = {key for key, value in choice.MESSAGE_EVENTS}


class Group(BaseModel):
    title = models.CharField(_("title"), max_length=50)

    class Meta:
        verbose_name = _("group")
        verbose_name_plural = _("groups")

    def __str__(self) -> str:
        return self.title


class GroupUser(BaseModel):
    group = models.ForeignKey("messaging.Group", verbose_name=_("group"), on_delete=models.CASCADE)
    user = models.ForeignKey("account.User", verbose_name=_("user"), on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("group user")
        verbose_name_plural = _("group users")
        unique_together = [("group", "user")]

    def __str__(self) -> str:
        return f"{self.group}( {self.user} )"


class GroupMessage(BaseModel):
    group = models.ForeignKey("messaging.Group", verbose_name=_("group"), on_delete=models.CASCADE)
    title = models.CharField(_("title"), max_length=50)
    content = models.TextField(_("content"))
    send_in_app = models.BooleanField(_("send in app"), default=False)
    send_notification = models.BooleanField(_("send notification"), default=False)
    send_email = models.BooleanField(_("send email"), default=False)
    send_sms = models.BooleanField(_("send sms"), default=False)

    class Meta:
        verbose_name = _("group message")
        verbose_name_plural = _("group messages")

    def __str__(self) -> str:
        return str(_("group message")) + f" #{self.id}"

    @hook(AFTER_CREATE)
    def create_child_messages(self):
        create_child_messages_for_group.delay(self.id)


class UserMessage(BaseModel):
    class SendType(models.IntegerChoices):
        SMS: int = 1
        EMAIL: int = 2
        IN_APP: int = 3
        NOTIFICATION: int = 4

    user = models.ForeignKey("account.User", verbose_name=_("user"), on_delete=models.CASCADE)
    title = models.CharField(_("title"), max_length=50)
    content = models.TextField(_("content"))
    send_in_app = models.BooleanField(_("send in app"), default=False)
    send_notification = models.BooleanField(_("send notification"), default=False)
    send_email = models.BooleanField(_("send email"), default=False)
    send_sms = models.BooleanField(_("send sms"), default=False)
    is_seen = models.BooleanField(_("is seen"), default=False)

    # we use this on method IN-App to redirect users when clicked on this message to
    # right place also we can pass this to a web point to generate right link to redirect
    event_type = models.SmallIntegerField(
        verbose_name=_("Event Type"),
        blank=True,
        editable=False,
        choices=choice.MESSAGE_EVENTS,
        default=choice.MESSAGE_EVENT_NOT_DEFINED,
        db_index=True,
    )

    # Json Should Be
    event_data = models.TextField(
        verbose_name=_("Event Data"),
        default="{}",
        blank=True,
        editable=False,
    )

    class Meta:
        verbose_name = _("user message")
        verbose_name_plural = _("user messages")

    def __str__(self) -> str:
        return str(_("user message")) + f" #{self.id}"

    @hook(AFTER_CREATE, when="send_notification", is_now=True)
    def handle_send_notification(self):
        send_notification_task.delay(self.user.id, self.title, self.content, self.event_type, self.event_data)

    @hook(AFTER_CREATE, when="send_email", is_now=True)
    def handle_send_email(self):
        email = self.user.email
        if email:
            send_email_task.delay(email, self.title, self.content)

    @hook(AFTER_CREATE, when="send_sms", is_now=True)
    def handle_send_sms(self):
        phone_number = self.user.phone_number
        if phone_number:
            send_simple_sms_task.delay(self.user.phone_number, self.content)

    @classmethod
    def send_message(cls, user, send_types: list[SendType], subject: str, message: str, event_type: int, event_data: str):
        if event_type not in MESSAGE_EVENT_KEYS:
            event_type = choice.MESSAGE_EVENT_NOT_DEFINED

        # Determine which types of notifications to send
        sms = cls.SendType.SMS in send_types
        email = cls.SendType.EMAIL in send_types
        in_app = cls.SendType.IN_APP in send_types
        notification = cls.SendType.NOTIFICATION in send_types

        obj = cls.objects.create(
            user=user,
            title=subject,
            content=message,
            send_in_app=in_app,
            send_notification=notification,
            send_email=email,
            send_sms=sms,
            event_type=event_type,
            event_data=event_data,
        )
        return obj


class UserDevice(BaseModel):
    user = models.ForeignKey("account.User", verbose_name=_("user"), on_delete=models.CASCADE)
    token = models.UUIDField(
        verbose_name=_("Token"),
        unique=True,
        db_index=True,
        editable=False,
    )
