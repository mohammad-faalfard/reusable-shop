"""a list of all messages in the system with subject and text"""

from django.utils.translation import gettext_lazy as _  # noqa: I001
from core import choice
from json import dumps

MESSAGE = str
SUBJECT = str
MESSAGE_EVENT = int
MESSAGE_EVENT_DATA = str

MessageTemplate = tuple[MESSAGE, SUBJECT, MESSAGE_EVENT, MESSAGE_EVENT_DATA]
event_data = dumps({"data": ""}, indent=0)


def expert_user_approve(name: str, user_id: int | None = None) -> MessageTemplate:
    subject: str = _("Your account status has changed")
    msg: str = _("Dear {name}, your account has been activated. You can now submit your responses!").format(name=name)
    event_data = dumps({"data": user_id}, indent=0)
    return subject, msg, choice.MESSAGE_EVENT_APPROVE_EXPERT, event_data


def expert_user_reject(name: str, user_id: int | None = None) -> MessageTemplate:
    subject: str = _("Your account status has changed")
    msg: str = _("Dear {name}, your account has been rejected by the shop moderator.").format(name=name)
    event_data = dumps({"data": user_id}, indent=0)
    return subject, msg, choice.MESSAGE_EVENT_REJECT_EXPERT, event_data


def expert_user_register(name: str, user_id: int | None = None) -> MessageTemplate:
    subject: str = _("Welcome to shop")
    msg: str = _(
        "Dear {name}, your information has been successfully registered. After approval by the shop moderator, your account will be activated."
    ).format(name=name)
    event_data = dumps({"data": user_id}, indent=0)
    return subject, msg, choice.MESSAGE_EVENT_NEW_EXPERT, event_data


def customer_register(name: str, user_id: int | None = None) -> MessageTemplate:
    subject: str = _("Welcome to shop")
    msg: str = _("Hello {name}, welcome to shop! Start asking questions and discovering answers right away.").format(
        name=name
    )
    event_data = dumps({"data": user_id}, indent=0)
    return subject, msg, choice.MESSAGE_EVENT_NEW_CUSTOMER, event_data


def question_receive_new_answer(question_slug: str, is_public: bool) -> MessageTemplate:
    subject: str = _("Notification")
    msg: str = _("A new answer has been posted for your question. Read it now!")
    event_data = dumps({"data": question_slug, "is_public": bool(is_public)}, indent=0)
    return subject, msg, choice.MESSAGE_EVENT_NEW_ANSWER, event_data


def medal_receive(medal_name: str, user_medal_id: int | None = None) -> MessageTemplate:
    subject: str = _("New Achievement")
    msg: str = _("Congratulations! You have successfully received the {medal_name} medal.").format(medal_name=medal_name)
    event_data = dumps({"data": user_medal_id}, indent=0)
    return subject, msg, choice.MESSAGE_EVENT_COMPLETE_TASK, event_data


def ticket_answer(subject: str, ticket_number: int) -> MessageTemplate:
    _subject: str = _("Notification")
    msg: str = _("A response has been posted for your ticket titled {subject}. Please check it.").format(subject=subject)
    event_data = dumps({"data": ticket_number}, indent=0)
    return _subject, msg, choice.MESSAGE_EVENT_ANSWER_TICKET, event_data


def ticket_close(subject: str, ticket_number: int) -> MessageTemplate:
    _subject: str = _("Notification")
    msg: str = _("Your ticket titled {subject} has been closed. We hope your issue has been fully resolved.").format(
        subject=subject
    )
    event_data = dumps({"data": ticket_number}, indent=0)
    return _subject, msg, choice.MESSAGE_EVENT_CLOSE_TICKET, event_data


def ticket_new(subject: str, ticket_number: int) -> MessageTemplate:
    _subject: str = _("New Ticket Notification")
    msg: str = _("A new ticket titled {subject} has been created. Please address it.").format(subject=subject)
    event_data = dumps({"data": ticket_number}, indent=0)
    return _subject, msg, choice.MESSAGE_EVENT_NEW_TICKET, event_data
