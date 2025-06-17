from django.urls import path
from .views import RoleListView, RoleDetailView, PermissionListView, UserRoleListView

app_name = 'administrator'

urlpatterns = [
    path('roles/', RoleListView.as_view(), name='role_list'),
    path('roles/<int:pk>/', RoleDetailView.as_view(), name='role_detail'),
    path('permissions/', PermissionListView.as_view(), name='permission_list'),
    path('userroles/', UserRoleListView.as_view(), name='userrole_list'),
]
