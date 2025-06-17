from django.views.generic import ListView, DetailView
from .models import Role, Permission, RolePermission, UserRole

class RoleListView(ListView):
    model = Role
    template_name = 'administrator/role_list.html'
    context_object_name = 'roles'

class RoleDetailView(DetailView):
    model = Role
    template_name = 'administrator/role_detail.html'
    context_object_name = 'role'

class PermissionListView(ListView):
    model = Permission
    template_name = 'administrator/permission_list.html'
    context_object_name = 'permissions'

class UserRoleListView(ListView):
    model = UserRole
    template_name = 'administrator/userrole_list.html'
    context_object_name = 'user_roles'
