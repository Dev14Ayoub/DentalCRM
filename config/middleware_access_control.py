from django.shortcuts import redirect
from django.urls import reverse
from administrator.models import UserRole

from django.shortcuts import redirect
from django.urls import reverse
from administrator.models import UserRole
from django.utils.deprecation import MiddlewareMixin

class AccessControlMiddleware(MiddlewareMixin):
    """
    Middleware to enforce access control based on authentication and user roles.

    - Unauthenticated users can only access login, register, services, and about pages.
    - Administrators have full access.
    - Doctors and office assistants have role-based access to specific pages.
    - Enforces clinic-level scoping by redirecting unauthorized access.
    """

    ALLOWED_PATHS_FOR_UNAUTHENTICATED = [
        '/users/login/',
        '/users/register/',
        '/services/',
        '/about/',
        '/users/api/login/',
        '/users/api/register/',
    ]

    def process_request(self, request):
        # Ensure AuthenticationMiddleware has run
        if not hasattr(request, 'user'):
            return None

        path = request.path

        # Debug prints to trace request path and user info
        print(f"AccessControlMiddleware: path={path}, user_authenticated={request.user.is_authenticated}, user={getattr(request.user, 'username', None)}")

        if not request.user.is_authenticated:
            # Allow only specific pages for unauthenticated users
            if not any(path.startswith(p) for p in self.ALLOWED_PATHS_FOR_UNAUTHENTICATED):
                print(f"AccessControlMiddleware: Redirecting unauthenticated user from {path} to login")
                return redirect(reverse('users:login'))
        else:
            # Authenticated user: check roles for access control
            user = request.user
            # Allow superusers full access including /admin
            if user.is_superuser:
                print(f"AccessControlMiddleware: Superuser {user.username} access granted to {path}")
                return None
            # Check if user is administrator
            if UserRole.objects.filter(user=user, role__name='administrator').exists():
                print(f"AccessControlMiddleware: Administrator {user.username} access granted to {path}")
                return None

            # Check if user is doctor
            if UserRole.objects.filter(user=user, role__name='doctor').exists():
                if path == '/users/logout' or path == '/users/logout/' or path.startswith('/doctors/') or path.startswith('/patients/') or path.startswith('/users/logout') or path.startswith('/users/logout/') or path.startswith('/users/profile/'):
                    print(f"AccessControlMiddleware: Doctor {user.username} access granted to {path}")
                    return None
                else:
                    print(f"AccessControlMiddleware: Doctor {user.username} access denied to {path}")
                    return redirect(reverse('users:login'))

            # Check if user is office assistant
            if UserRole.objects.filter(user=user, role__name='office_assistant').exists():
                if path.startswith('/office_assistant/') or path.startswith('/users/logout/') or path.startswith('/users/profile/') or path.startswith('/patients/'):
                    print(f"AccessControlMiddleware: Office assistant {user.username} access granted to {path}")
                    return None
                else:
                    print(f"AccessControlMiddleware: Office assistant {user.username} access denied to {path}")
                    return redirect(reverse('users:login'))

            # For other authenticated users, allow access to general pages or deny
            allowed_general_paths = [
                '/users/logout/',
                '/users/profile/',
                '/patients/',
                '/schedule/',
                '/leads/',
                '/clinic/',
                '/base/',
            ]
            if any(path.startswith(p) for p in allowed_general_paths):
                print(f"AccessControlMiddleware: User {user.username} access granted to {path}")
                return None

            print(f"AccessControlMiddleware: User {user.username} access denied to {path}")
            return redirect(reverse('users:login'))

        # Default: proceed with request
        return None
