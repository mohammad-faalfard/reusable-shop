import logging
from datetime import datetime, timedelta, timezone
from json import dumps as json_dumps

import pytz
import requests

from .api_setting import NAJVA_APIKEY, NAJVA_TOKEN

LIMIT_BODY: int = 200
LIMIT_TITLE: int = 100
# Iran TimeZone
TH = pytz.timezone("Asia/Tehran")

logger = logging.getLogger("notification")


## api to send notification for specific users
def send_to_users_API(
    title: str,
    body: str,
    url: str,
    icon: str,
    subscriber_tokens: list[str],
    image: str | None = None,
    content: str | None = None,
    json: dict | None = None,
) -> int:
    """send push notif via Najva API"""

    json: dict = json or {}
    json: str = json_dumps(json)
    body = body[:LIMIT_BODY]
    title = title[:LIMIT_TITLE]
    utc_dt: datetime = datetime.now(timezone.utc) + timedelta(seconds=30)
    # base on iran timezone
    sent_time: str = utc_dt.astimezone(TH).strftime("%Y-%m-%dT%H:%M:%S")

    api_url: str = "https://app.najva.com/api/v2/notification/management/send-direct/"

    data: dict = {
        "title": title,
        "body": body,
        "onclick_action": 0,  # Open-Link
        "url": url,
        "content": content,
        "icon": icon,
        "image": image,
        "utm": {},
        "json": json,
        "light_up_screen": False,
        "buttons": [],
        "subscribers": subscriber_tokens,
        "sent_time": sent_time,
    }

    headers: dict = {
        "content-type": "application/json",
        "cache-control": "no-cache",
        "x-api-key": NAJVA_APIKEY,
        "authorization": f"Token {NAJVA_TOKEN}",
    }

    response = requests.post(
        url=api_url,
        json=data,
        headers=headers,
        timeout=60,
    )
    logger.debug([headers, data, response.json()])

    return response.status_code


def send_notification(receivers: list[str], title: str, content: str, url: str) -> int:
    resp = send_to_users_API(
        title=title,
        body=content,
        url=url,
        # Icon and Image Push-Notif shows to users
        icon="",
        image="",
        subscriber_tokens=receivers,
    )

    return resp
