from django.http import HttpRequest
from django.templatetags.static import static


def get_full_static_url(request: HttpRequest, relative_url: str) -> str:
    """
    Constructs the full static URL for a given relative path.

    Args:
        request (HttpRequest): The HTTP request object.
        relative_url (str): The relative path to the static asset.

    Returns:
        str: Full URL to the static asset.
    """
    static_url = static(relative_url)  # e.g., '/static/icons/facebook.png'
    full_url = request.build_absolute_uri(static_url)  # e.g., 'https://website.com/static/icons/facebook.png'
    return full_url
