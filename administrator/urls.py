from django.urls import path
from .views import RoleListView, RoleDetailView, PermissionListView, UserRoleListView
from . import views_rbac

app_name = 'administrator'

urlpatterns = [
    path('roles/', RoleListView.as_view(), name='role_list'),
    path('roles/<int:pk>/', RoleDetailView.as_view(), name='role_detail'),
    path('permissions/', PermissionListView.as_view(), name='permission_list'),
    path('userroles/', UserRoleListView.as_view(), name='userrole_list'),

    # RBAC management views
    path('rbac/', views_rbac.rbac_management, name='rbac_management'),
    path('rbac/toggle_user_role/', views_rbac.toggle_user_role, name='toggle_user_role'),
    path('rbac/toggle_role_permission/', views_rbac.toggle_role_permission, name='toggle_role_permission'),
]
