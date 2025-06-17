import logging
from django.test import TestCase, Client
from django.contrib.auth.models import User, Group, Permission
from django.urls import reverse
from unittest.mock import patch

class AuditLoggingMiddlewareTests(TestCase):
    def setUp(self):
        self.client = Client()
        # Create group with patient view permission
        self.group = Group.objects.create(name='TestGroup')
        view_patient_perm = Permission.objects.get(codename='view_patient')
        self.group.permissions.add(view_patient_perm)
        # Create user and assign group
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.user.groups.add(self.group)

    @patch('patient.middleware.audit_logging.logger')
    def test_audit_logging_anonymous_user(self, mock_logger):
        response = self.client.get(reverse('patient:list'))
        self.assertEqual(response.status_code, 302)  # Redirect to login or permission denied
        self.assertTrue(mock_logger.info.called)
        log_msg = mock_logger.info.call_args[0][0]
        self.assertIn('GET', log_msg)
        self.assertIn('/patients/', log_msg)
        self.assertIn('anonymous user', log_msg)

    @patch('patient.middleware.audit_logging.logger')
    def test_audit_logging_authenticated_user(self, mock_logger):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('patient:list'))
        self.assertIn(response.status_code, [200, 403])  # Depending on permissions
        self.assertTrue(mock_logger.info.called)
        log_msg = mock_logger.info.call_args[0][0]
        self.assertIn('GET', log_msg)
        self.assertIn('/patients/', log_msg)
        self.assertIn('user=testuser', log_msg)
