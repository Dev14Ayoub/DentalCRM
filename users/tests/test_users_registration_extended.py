from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User
from users.models import Profile
from clinic.models import Clinic
from administrator.models import Role, UserRole

class UserRegistrationExtendedTests(TestCase):
    def setUp(self):
        # Create administrator role if not exists
        self.admin_role, _ = Role.objects.get_or_create(name='administrator')

    def test_profile_photo_upload_on_registration(self):
        url = reverse('users:create')
        photo = SimpleUploadedFile(
            name='test_photo.jpg',
            content=b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\xff\xff\xff\x21\xf9\x04\x01\x00\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x4c\x01\x00\x3b',
            content_type='image/jpeg'
        )
        form_data = {
            'first_name': 'Admin',
            'last_name': 'User',
            'username': 'userphoto',  # Changed username to avoid forbidden username 'admin'
            'email': 'adminphoto@example.com',
            'password1': 'Str0ngPa$$word1',
            'password2': 'Str0ngPa$$word1',
            'clinic': 'Photo Clinic',
            'phone_number': '1234567890',
            'photo': photo,
        }
        response = self.client.post(url, data=form_data, follow=True)
        self.assertEqual(response.status_code, 200)
        user = User.objects.get(username='userphoto')
        self.assertIsNotNone(user.profile.photo)
        self.assertTrue(user.profile.photo.name.startswith('profile_photos/'))

    def test_clinic_association_and_administrator_role(self):
        url = reverse('users:create')
        form_data = {
            'first_name': 'Admin',
            'last_name': 'User',
            'username': 'userclinic',  # Changed username to avoid forbidden username 'admin'
            'email': 'adminclinic@example.com',
            'password1': 'Str0ngPa$$word2',
            'password2': 'Str0ngPa$$word2',
            'clinic': 'Clinic Association',
            'phone_number': '0987654321',
        }
        response = self.client.post(url, data=form_data, follow=True)
        self.assertEqual(response.status_code, 200)
        user = User.objects.get(username='userclinic')
        clinic = Clinic.objects.get(name='Clinic Association')
        self.assertEqual(user.profile.clinic, clinic)
        # Check administrator role assignment
        user_role = UserRole.objects.filter(user=user, role=self.admin_role).first()
        self.assertIsNotNone(user_role)

    def test_critical_path_registration_and_login(self):
        # Register user
        url_register = reverse('users:create')
        form_data = {
            'first_name': 'Critical',
            'last_name': 'Path',
            'username': 'criticaluser',
            'email': 'critical@example.com',
            'password1': 'Str0ngPa$$word3',
            'password2': 'Str0ngPa$$word3',
            'clinic': 'Critical Clinic',
            'phone_number': '1112223333',
        }
        response = self.client.post(url_register, data=form_data, follow=True)
        self.assertEqual(response.status_code, 200)
        user = User.objects.get(username='criticaluser')

        # Login user
        url_login = reverse('users:login_create')
        login_data = {
            'username': 'criticaluser',
            'password': 'Str0ngPa$$word3',
        }
        response = self.client.post(url_login, data=login_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('_auth_user_id' in self.client.session)
