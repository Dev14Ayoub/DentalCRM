import logging
from django.utils.deprecation import MiddlewareMixin
from django.utils.timezone import now

class AuditLoggingMiddleware(MiddlewareMixin):
    def __init__(self, get_response=None, logger=None):
        self.get_response = get_response
        self.logger = logger or logging.getLogger('audit')
        super().__init__(get_response)

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else None
        method = request.method
        path = request.get_full_path()
        timestamp = now().isoformat()
        user_info = f'user={user.username}' if user else 'anonymous user'
        print(f"AuditLoggingMiddleware: Logging {method} {path} for {user_info}")  # Debug print
        self.logger.info(f"[{timestamp}] {method} {path} {user_info}")
        response = self.get_response(request)
        return response

