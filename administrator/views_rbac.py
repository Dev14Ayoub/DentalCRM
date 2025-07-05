from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST
from administrator.models import Role, Permission, RolePermission, UserRole
from django.contrib.auth.models import User

def is_administrator(user):
    # Check if user has administrator role only, ignoring superuser/staff flags
    return UserRole.objects.filter(user=user, role__name='administrator').exists()

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST
from administrator.models import Role, Permission, RolePermission, UserRole
from django.contrib.auth.models import User
from functools import wraps

def is_administrator(user):
    # Check if user has administrator role
    return UserRole.objects.filter(user=user, role__name='administrator').exists()

def admin_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            from django.contrib.auth.views import redirect_to_login
            return redirect_to_login(request.get_full_path())
        if not is_administrator(request.user):
            return HttpResponseForbidden("You do not have permission to access this resource.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view

@login_required
@admin_required
def rbac_management(request):
    users = User.objects.all().prefetch_related('userrole_set__role')
    roles = Role.objects.all().prefetch_related('rolepermission_set__permission')
    permissions = Permission.objects.all()
    user_roles = UserRole.objects.select_related('user', 'role')
    role_permissions = RolePermission.objects.select_related('role', 'permission')

    context = {
        'users': users,
        'roles': roles,
        'permissions': permissions,
        'user_roles': user_roles,
        'role_permissions': role_permissions,
    }
    return render(request, 'administrator/rbac_management.html', context)

@login_required
@admin_required
@require_POST
def toggle_user_role(request):
    user_id = request.POST.get('user_id')
    role_id = request.POST.get('role_id')
    action = request.POST.get('action')  # 'assign' or 'revoke'

    if not user_id or not role_id or action not in ['assign', 'revoke']:
        return JsonResponse({'success': False, 'error': 'Invalid parameters'})

    user = get_object_or_404(User, id=user_id)
    role = get_object_or_404(Role, id=role_id)

    if action == 'assign':
        UserRole.objects.get_or_create(user=user, role=role)
    else:
        UserRole.objects.filter(user=user, role=role).delete()

    return JsonResponse({'success': True})

@login_required
@admin_required
@require_POST
def toggle_role_permission(request):
    role_id = request.POST.get('role_id')
    permission_id = request.POST.get('permission_id')
    action = request.POST.get('action')  # 'assign' or 'revoke'

    if not role_id or not permission_id or action not in ['assign', 'revoke']:
        return JsonResponse({'success': False, 'error': 'Invalid parameters'})

    role = get_object_or_404(Role, id=role_id)
    permission = get_object_or_404(Permission, id=permission_id)

    if action == 'assign':
        RolePermission.objects.get_or_create(role=role, permission=permission)
    else:
        RolePermission.objects.filter(role=role, permission=permission).delete()

    return JsonResponse({'success': True})
