def get_client_ip(request):
    """
    Returns requested client ip
    """
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    ip = x_forwarded_for.split(",")[0] if x_forwarded_for else request.META.get("REMOTE_ADDR")

    return ip


def get_session_key(request):
    # Access the session to ensure a session key is generated
    session_key = request.session.session_key

    # If the session key doesn't exist, create one
    if not session_key:
        request.session.create()
        session_key = request.session.session_key
    return session_key


def get_user(request):
    if request and request.user.is_authenticated:
        return request.user
    return None
