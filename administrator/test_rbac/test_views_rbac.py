import unittest
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from administrator.models import Role, Permission, RolePermission, UserRole


class TestRbacViews(TestCase):
    def setUp(self):
        # Create test user and roles/permissions
        self.admin_user = User.objects.create_user(username='admin', password='adminpass')
        self.normal_user = User.objects.create_user(username='user', password='userpass')

        self.admin_role = Role.objects.create(name='administrator')
        self.user_role = Role.objects.create(name='user')

        self.permission1 = Permission.objects.create(name='Can View', codename='can_view')
        self.permission2 = Permission.objects.create(name='Can Edit', codename='can_edit')

        RolePermission.objects.create(role=self.admin_role, permission=self.permission1)
        RolePermission.objects.create(role=self.admin_role, permission=self.permission2)

        UserRole.objects.create(user=self.admin_user, role=self.admin_role)

        self.client = Client()

    def test_rbac_management_access(self):
        # Unauthenticated user redirected to login
        response = self.client.get(reverse('administrator:rbac_management'))
        self.assertEqual(response.status_code, 302)

        # Normal user forbidden - ensure user is authenticated but lacks permission
        self.client.login(username='user', password='userpass')
        # Remove all roles/permissions from normal user to simulate lack of permission
        from administrator.models import UserRole
        UserRole.objects.filter(user__username='user').delete()
        response = self.client.get(reverse('administrator:rbac_management'))
        self.assertEqual(response.status_code, 403)
        self.client.logout()

        # Admin user can access
        self.client.login(username='admin', password='adminpass')
        response = self.client.get(reverse('administrator:rbac_management'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'RBAC Management')
        self.client.logout()

    def test_toggle_user_role_assign_and_revoke(self):
        self.client.login(username='admin', password='adminpass')
        url = reverse('administrator:toggle_user_role')

        # Assign role to normal user
        response = self.client.post(url, {'user_id': self.normal_user.id, 'role_id': self.user_role.id, 'action': 'assign'})
        self.assertJSONEqual(response.content, {'success': True})
        self.assertTrue(UserRole.objects.filter(user=self.normal_user, role=self.user_role).exists())

        # Revoke role from normal user
        response = self.client.post(url, {'user_id': self.normal_user.id, 'role_id': self.user_role.id, 'action': 'revoke'})
        self.assertJSONEqual(response.content, {'success': True})
        self.assertFalse(UserRole.objects.filter(user=self.normal_user, role=self.user_role).exists())

        self.client.logout()

    def test_toggle_role_permission_assign_and_revoke(self):
        self.client.login(username='admin', password='adminpass')
        url = reverse('administrator:toggle_role_permission')

        # Assign permission to user_role
        response = self.client.post(url, {'role_id': self.user_role.id, 'permission_id': self.permission1.id, 'action': 'assign'})
        self.assertJSONEqual(response.content, {'success': True})
        self.assertTrue(RolePermission.objects.filter(role=self.user_role, permission=self.permission1).exists())

        # Revoke permission from user_role
        response = self.client.post(url, {'role_id': self.user_role.id, 'permission_id': self.permission1.id, 'action': 'revoke'})
        self.assertJSONEqual(response.content, {'success': True})
        self.assertFalse(RolePermission.objects.filter(role=self.user_role, permission=self.permission1).exists())

        self.client.logout()

    def test_toggle_user_role_invalid_params(self):
        self.client.login(username='admin', password='adminpass')
        url = reverse('administrator:toggle_user_role')

        response = self.client.post(url, {'user_id': '', 'role_id': '', 'action': 'assign'})
        self.assertJSONEqual(response.content, {'success': False, 'error': 'Invalid parameters'})

        response = self.client.post(url, {'user_id': self.normal_user.id, 'role_id': self.user_role.id, 'action': 'invalid'})
        self.assertJSONEqual(response.content, {'success': False, 'error': 'Invalid parameters'})

        self.client.logout()

    def test_toggle_role_permission_invalid_params(self):
        self.client.login(username='admin', password='adminpass')
        url = reverse('administrator:toggle_role_permission')

        response = self.client.post(url, {'role_id': '', 'permission_id': '', 'action': 'assign'})
        self.assertJSONEqual(response.content, {'success': False, 'error': 'Invalid parameters'})

        response = self.client.post(url, {'role_id': self.user_role.id, 'permission_id': self.permission1.id, 'action': 'invalid'})
        self.assertJSONEqual(response.content, {'success': False, 'error': 'Invalid parameters'})

        self.client.logout()

    def test_permission_required_for_toggle_views(self):
        url_user_role = reverse('administrator:toggle_user_role')
        url_role_permission = reverse('administrator:toggle_role_permission')

        # Unauthenticated user redirected
        response = self.client.post(url_user_role, {})
        self.assertEqual(response.status_code, 302)
        response = self.client.post(url_role_permission, {})
        self.assertEqual(response.status_code, 302)

        # Normal user forbidden - ensure user is authenticated but lacks permission
        self.client.login(username='user', password='userpass')
        from administrator.models import UserRole
        UserRole.objects.filter(user__username='user').delete()
        response = self.client.post(url_user_role, {})
        self.assertEqual(response.status_code, 403)
        response = self.client.post(url_role_permission, {})
        self.assertEqual(response.status_code, 403)
        self.client.logout()

if __name__ == '__main__':
    unittest.main()
