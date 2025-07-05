from django.shortcuts import redirect
from django.urls import reverse

class PasswordChangeRequiredMiddleware:
    """
    Middleware to force users to change their password on first login or when required.
    Checks the 'must_change_password' flag on the user's profile.
    Redirects to password change page if flag is True.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated:
            return self.get_response(request)

        # Allow access to password change and logout views without redirect
        allowed_paths = [
            reverse('users:change_password'),
            reverse('users:logout'),
        ]
        if request.path in allowed_paths:
            return self.get_response(request)

        # Check if user must change password
        if hasattr(request.user, 'profile') and request.user.profile.must_change_password:
            return redirect(reverse('users:change_password'))

        return self.get_response(request)
