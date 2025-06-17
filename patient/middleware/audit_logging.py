import logging
from django.utils.deprecation import MiddlewareMixin
from django.utils.timezone import now

logger = logging.getLogger('audit')

class AuditLoggingMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        user = request.user if request.user.is_authenticated else None
        method = request.method
        path = request.get_full_path()
        timestamp = now().isoformat()
        user_info = f'user={user.username}' if user else 'anonymous user'
        logger.info(f"[{timestamp}] {method} {path} {user_info}")
        return None
