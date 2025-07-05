from django.conf import settings

class AdminSessionMiddleware:
    """
    Middleware to use a separate session cookie for Django admin (/admin) and frontend.

    Sets SESSION_COOKIE_NAME to 'admin_sessionid' for /admin paths,
    and 'sessionid' for other paths.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/admin'):
            settings.SESSION_COOKIE_NAME = 'admin_sessionid'
        else:
            settings.SESSION_COOKIE_NAME = 'sessionid'
        response = self.get_response(request)
        return response
