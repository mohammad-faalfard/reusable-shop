from threading import local

# Thread-local storage for current user
_thread_locals = local()


def get_current_user():
    """
    Retrieves the current user stored in thread-local storage.
    Returns None if no user is set, making it safe to call globally.
    """
    return getattr(_thread_locals, "user", None)


class ThreadLocalUserMiddleware:
    """
    Middleware to save the current user in thread-local storage,
    making it accessible globally during the request lifecycle.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Store the current user in thread-local storage
        _thread_locals.user = getattr(request, "user", None)

        # Proceed with the request and get the response
        response = self.get_response(request)

        # Clean up thread-local storage to avoid memory leaks
        _thread_locals.user = None

        return response
