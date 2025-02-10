from kavenegar import APIException, HTTPException, KavenegarAPI

from .api_setting import KAVENEGAR_APIKEY

api = KavenegarAPI(KAVENEGAR_APIKEY)


def sms_character_replace(text: str) -> str:
    """
    replace space in text to send by kavenegar
    :param text: text
    :type text: str
    :return: replaced space text
    :rtype: str
    """
    return str(text).replace(" ", "‌").replace("_", "-")  # kavenegar error 431


def send_simple_sms(receptor: str, message: str):
    try:
        params = {
            "receptor": receptor,
            "message": message,
        }
        response = api.sms_send(params)
        print(response)
    except APIException as e:
        print(e)
    except HTTPException as e:
        print(e)


def send_tokened_sms(receptor: str, template: str, tokens: list):
    try:
        params = {
            "receptor": receptor,
            "template": template,
            "type": "sms",
        }
        for index, token in enumerate(tokens):
            if index == 0:
                params["token"] = sms_character_replace(token)
            else:
                params[f"token{index + 1}"] = sms_character_replace(token)

        response = api.verify_lookup(params)
        print(response)
    except APIException as e:
        print(e)
    except HTTPException as e:
        print(e)
