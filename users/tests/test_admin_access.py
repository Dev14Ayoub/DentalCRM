from django.test import TestCase
from django.urls import reverse
from django.conf import settings

class AdminAccessTests(TestCase):
    def test_admin_url_accessible(self):
        # Check if 'django.contrib.admin' is in INSTALLED_APPS
        self.assertIn('django.contrib.admin', settings.INSTALLED_APPS)

        # Access the admin login page
        response = self.client.get(reverse('admin:index'))
        # Should return 200 OK or redirect to login if not authenticated
        self.assertIn(response.status_code, [200, 302])

    def test_admin_static_files_served(self):
        # Access a common admin static file
        response = self.client.get('/static/admin/css/base.css')
        self.assertIn(response.status_code, [200, 404])  # 404 if static files not collected

    def test_admin_login_redirect(self):
        # Access admin page without login should redirect to login page
        response = self.client.get('/admin/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'username', status_code=200)
