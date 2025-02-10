from json import JSONDecodeError, loads

from django.conf import settings
from django.contrib.auth import get_user_model

from core import choice

User = get_user_model()
SITE_URL: str = settings.SITE_URL


def question_url(is_public: bool, slug: str) -> str:
    "relative url for question page on fronted"

    if not slug:
        return "questions/"
    elif not is_public:
        return f"questions/private/{slug}"
    elif is_public:
        return f"questions/public/{slug}"
    else:
        return f"questions/private/{slug}"


def ticket_url(ticket_number: int | str) -> str:
    "relative URL for ticket in fronted"
    if ticket_number:
        return f"tickets/{ticket_number}"
    else:
        return "tickets/"


def task_url() -> str:
    return "scores/"


def map_event_to_front(event_type: int, event_data: str | None, user_id: int) -> str:
    """This func generate a front-end URL for an event to send to users

    Args:
        event (int): Event code
        data (str|None): Data of event can be any string or None but mostly is a JSON
        user (_type_): The user the event occurred for it
    """

    user = User.objects.get(pk=user_id)

    # base url for fronted
    base_url: str = str(SITE_URL).strip("/") + "/"
    expert_dashboard_address: str = base_url + "expert/dashboard/"
    customer_dashboard_address: str = base_url + "user/dashboard/"
    dashboard_url: str = {
        choice.USER_TYPE_EXPERT: expert_dashboard_address,
        choice.USER_TYPE_ADMIN: expert_dashboard_address,
        choice.USER_TYPE_CUSTOMER: customer_dashboard_address,
        choice.USER_TYPE_NOT_DEFINED: customer_dashboard_address,
    }.get(user.type, customer_dashboard_address)

    final_url: str = dashboard_url

    try:
        event_data: dict = loads(event_data)
    except TypeError:
        event_data: dict = {}
    except JSONDecodeError:
        event_data: dict = {}

    match event_type:
        case (
            choice.MESSAGE_EVENT_NEW_ANSWER
            | choice.MESSAGE_EVENT_QUESTION
            | choice.MESSAGE_EVENT_NEW_QUESTION
            | choice.MESSAGE_EVENT_RECEIVE_QUESTION
        ):
            question_type: bool = event_data.get("is_public", True)
            question_slug: str = event_data.get("data", "")
            final_url += question_url(question_type, question_slug)

        case choice.MESSAGE_EVENT_NEW_TICKET | choice.MESSAGE_EVENT_ANSWER_TICKET | choice.MESSAGE_EVENT_CLOSE_TICKET:
            ticket_number: int | str = event_data.get("data", "")
            final_url += ticket_url(ticket_number)

        case choice.MESSAGE_EVENT_COMPLETE_TASK:
            final_url += task_url()

        case choice.MESSAGE_EVENT_NOT_DEFINED:
            ...
        case choice.MESSAGE_EVENT_NEW_CUSTOMER:
            ...
        case choice.MESSAGE_EVENT_NEW_EXPERT:
            ...
        case choice.MESSAGE_EVENT_REJECT_REPORT:
            ...
        case choice.MESSAGE_EVENT_APPROVE_EXPERT:
            ...
        case choice.MESSAGE_EVENT_REJECT_EXPERT:
            ...

    return final_url
