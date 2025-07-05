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

    def test_audit_logging_anonymous_user(self):
        from patient.middleware.audit_logging import AuditLoggingMiddleware
        from unittest.mock import Mock
        mock_logger = Mock()
        mock_get_response = Mock()
        middleware = AuditLoggingMiddleware(get_response=mock_get_response, logger=mock_logger)
        mock_request = Mock()
        mock_request.user.is_authenticated = False
        mock_request.method = 'GET'
        mock_request.get_full_path.return_value = '/patients/'
        response_mock = Mock()
        mock_get_response.return_value = response_mock

        result = middleware(mock_request)

        mock_logger.info.assert_called_once()
        log_msg = mock_logger.info.call_args[0][0]
        print(f"Test: audit_logging_anonymous_user logged message: {log_msg}")
        self.assertIn('GET', log_msg)
        self.assertIn('/patients/', log_msg)
        self.assertIn('anonymous user', log_msg)
        self.assertEqual(result, response_mock)

    def test_audit_logging_authenticated_user(self):
        from patient.middleware.audit_logging import AuditLoggingMiddleware
        from unittest.mock import Mock
        mock_logger = Mock()
        mock_get_response = Mock()
        middleware = AuditLoggingMiddleware(get_response=mock_get_response, logger=mock_logger)
        mock_request = Mock()
        mock_request.user.is_authenticated = True
        mock_request.user.username = 'testuser'
        mock_request.method = 'GET'
        mock_request.get_full_path.return_value = '/patients/'
        response_mock = Mock()
        mock_get_response.return_value = response_mock

        result = middleware(mock_request)

        mock_logger.info.assert_called_once()
        log_msg = mock_logger.info.call_args[0][0]
        print(f"Test: audit_logging_authenticated_user logged message: {log_msg}")
        self.assertIn('GET', log_msg)
        self.assertIn('/patients/', log_msg)
        self.assertIn('user=testuser', log_msg)
        self.assertEqual(result, response_mock)

    def test_middleware_logging_direct_call(self):
        from patient.middleware.audit_logging import AuditLoggingMiddleware
        from unittest.mock import Mock
        mock_logger = Mock()
        mock_get_response = Mock()
        middleware = AuditLoggingMiddleware(get_response=mock_get_response, logger=mock_logger)
        mock_request = Mock()
        mock_request.user.is_authenticated = True
        mock_request.user.username = 'testuser'
        mock_request.method = 'GET'
        mock_request.get_full_path.return_value = '/patients/'
        response_mock = Mock()
        mock_get_response.return_value = response_mock

        result = middleware(mock_request)

        mock_logger.info.assert_called_once()
        log_msg = mock_logger.info.call_args[0][0]
        print(f"Middleware direct call logged message: {log_msg}")
        self.assertIn('GET', log_msg)
        self.assertIn('/patients/', log_msg)
        self.assertIn('user=testuser', log_msg)
        self.assertEqual(result, response_mock)

    def test_middleware_logging_direct_call_anonymous(self):
        from patient.middleware.audit_logging import AuditLoggingMiddleware
        from unittest.mock import Mock
        mock_logger = Mock()
        mock_get_response = Mock()
        middleware = AuditLoggingMiddleware(get_response=mock_get_response, logger=mock_logger)
        mock_request = Mock()
        mock_request.user.is_authenticated = False
        mock_request.method = 'POST'
        mock_request.get_full_path.return_value = '/patients/create/'
        response_mock = Mock()
        mock_get_response.return_value = response_mock

        result = middleware(mock_request)

        mock_logger.info.assert_called_once()
        log_msg = mock_logger.info.call_args[0][0]
        print(f"Middleware direct call logged message (anonymous): {log_msg}")
        self.assertIn('POST', log_msg)
        self.assertIn('/patients/create/', log_msg)
        self.assertIn('anonymous user', log_msg)
        self.assertEqual(result, response_mock)
