from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from administrator.models import Role, UserRole

class AccessControlMiddlewareTests(TestCase):
    def setUp(self):
        # Create users
        self.admin_user = User.objects.create_user(username='admin', password='adminpass')
        self.doctor_user = User.objects.create_user(username='doctor', password='doctorpass')
        self.office_assistant_user = User.objects.create_user(username='assistant', password='assistantpass')
        self.normal_user = User.objects.create_user(username='user', password='userpass')

        # Create roles
        self.admin_role = Role.objects.create(name='administrator')
        self.doctor_role = Role.objects.create(name='doctor')
        self.office_assistant_role = Role.objects.create(name='office_assistant')

        # Assign roles
        UserRole.objects.create(user=self.admin_user, role=self.admin_role)
        UserRole.objects.create(user=self.doctor_user, role=self.doctor_role)
        UserRole.objects.create(user=self.office_assistant_user, role=self.office_assistant_role)

        self.client = Client()

    def test_unauthenticated_user_access(self):
        # Allowed pages for unauthenticated users
        allowed_urls = [
            reverse('users:login'),
            reverse('users:register'),
            '/services/',
            '/about/',
        ]
        for url in allowed_urls:
            response = self.client.get(url)
            self.assertNotEqual(response.status_code, 302, f"Unauthenticated user should access {url}")

        # Disallowed page
        response = self.client.get('/patients/')
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('users:login'), response.url)

    def test_admin_user_full_access(self):
        self.client.login(username='admin', password='adminpass')
        # Admin should access any page, test a few
        urls = [
            '/patients/',
            '/doctors/',
            '/office_assistant/',
            '/administrator/',
        ]
        for url in urls:
            response = self.client.get(url)
            self.assertNotEqual(response.status_code, 302, f"Admin should access {url}")

    def test_doctor_user_access(self):
        self.client.login(username='doctor', password='doctorpass')
        # Allowed pages for doctor
        allowed_urls = [
            '/doctors/',
            '/users/logout/',
            '/users/profile/',
            '/patients/',
        ]
        for url in allowed_urls:
            response = self.client.get(url)
            # Allow 200 or 302 for logout URL since logout redirects
            if url == '/users/logout/':
                self.assertIn(response.status_code, [200, 302], f"Doctor should access {url}")
            else:
                self.assertNotEqual(response.status_code, 302, f"Doctor should access {url}")

        # Test logout redirects to login page (302)
        response = self.client.get('/users/logout/')
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('users:login'), response.url)

    def test_office_assistant_user_access(self):
        self.client.login(username='assistant', password='assistantpass')
        # Allowed pages for office assistant
        allowed_urls = [
            '/office_assistant/',
            '/users/logout/',
            '/users/profile/',
            '/patients/',
        ]
        for url in allowed_urls:
            response = self.client.get(url)
            # Allow 200 or 302 for logout URL since logout redirects
            if url == '/users/logout/':
                self.assertIn(response.status_code, [200, 302], f"Office assistant should access {url}") 
            else:
                self.assertNotEqual(response.status_code, 302, f"Office assistant should access {url}")  

        # Test logout redirects to login page (302)
        response = self.client.get('/users/logout/')
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('users:login'), response.url)

    def test_normal_user_access(self):
        self.client.login(username='user', password='userpass')
        # Allowed general pages
        allowed_urls = [
            '/users/logout/',
            '/users/profile/',
            '/patients/',
            '/schedule/',
            '/leads/',
            '/clinic/',
            '/base/',
            '/doctors/',
        ]
        for url in allowed_urls:
            response = self.client.get(url)
            # Allow 200 or 302 for logout URL since logout redirects
            if url == '/users/logout/':
                self.assertIn(response.status_code, [200, 302], f"Normal user should access {url}")
            else:
                self.assertNotEqual(response.status_code, 302, f"Normal user should access {url}")

        # Test logout redirects to login page (302)
        response = self.client.get('/users/logout/')
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('users:login'), response.url)
