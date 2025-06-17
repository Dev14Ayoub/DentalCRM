from django.test import TestCase, Client
from django.contrib.auth.models import User, Group, Permission
from django.urls import reverse
from patient.models import Patient

class RBACPermissionTests(TestCase):
    def setUp(self):
        # Create groups
        self.admin_group = Group.objects.create(name='Administrator')
        self.doctor_group = Group.objects.create(name='Doctor')
        self.office_assistant_group = Group.objects.create(name='Office Assistant')
        self.lead_group = Group.objects.create(name='Lead')

        # Create permissions
        view_patient_perm = Permission.objects.get(codename='view_patient')
        add_patient_perm = Permission.objects.get(codename='add_patient')
        change_patient_perm = Permission.objects.get(codename='change_patient')
        delete_patient_perm = Permission.objects.get(codename='delete_patient')

        # Assign permissions to groups
        self.admin_group.permissions.set(Permission.objects.all())
        self.doctor_group.permissions.set([view_patient_perm, change_patient_perm])
        self.office_assistant_group.permissions.set([view_patient_perm])
        self.lead_group.permissions.set([])  # No patient permissions

        # Create users
        self.admin_user = User.objects.create_user(username='admin', password='adminpass')
        self.admin_user.groups.add(self.admin_group)

        self.doctor_user = User.objects.create_user(username='doctor', password='doctorpass')
        self.doctor_user.groups.add(self.doctor_group)

        self.office_assistant_user = User.objects.create_user(username='assistant', password='assistantpass')
        self.office_assistant_user.groups.add(self.office_assistant_group)

        self.lead_user = User.objects.create_user(username='lead', password='leadpass')
        self.lead_user.groups.add(self.lead_group)

        # Create a patient for admin user
        self.patient = Patient.objects.create(
            first_name='John',
            last_name='Doe',
            phone='1234567890',
            email='john@example.com',
            date_of_birth='1990-01-01',
            created_by=self.admin_user
        )
        # Create a patient for doctor user for doctor access tests
        self.doctor_patient = Patient.objects.create(
            first_name='Jane',
            last_name='Smith',
            phone='0987654321',
            email='jane@example.com',
            date_of_birth='1985-05-05',
            created_by=self.doctor_user
        )

        self.client = Client()

    def test_admin_access(self):
        self.client.login(username='admin', password='adminpass')
        response = self.client.get(reverse('patient:list'))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('patient:create'))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('patient:update', args=[self.patient.id]))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('patient:delete', args=[self.patient.id]))
        self.assertEqual(response.status_code, 200)

    def test_doctor_access(self):
        self.client.login(username='doctor', password='doctorpass')
        response = self.client.get(reverse('patient:list'))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('patient:create'))
        self.assertEqual(response.status_code, 403)  # No add permission
        response = self.client.get(reverse('patient:update', args=[self.doctor_patient.id]))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('patient:delete', args=[self.doctor_patient.id]))
        self.assertEqual(response.status_code, 403)  # No delete permission

    def test_office_assistant_access(self):
        self.client.login(username='assistant', password='assistantpass')
        response = self.client.get(reverse('patient:list'))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('patient:create'))
        self.assertEqual(response.status_code, 403)
        response = self.client.get(reverse('patient:update', args=[self.patient.id]))
        self.assertEqual(response.status_code, 403)
        response = self.client.get(reverse('patient:delete', args=[self.patient.id]))
        self.assertEqual(response.status_code, 403)

    def test_lead_access(self):
        self.client.login(username='lead', password='leadpass')
        response = self.client.get(reverse('patient:list'))
        self.assertEqual(response.status_code, 403)
        response = self.client.get(reverse('patient:create'))
        self.assertEqual(response.status_code, 403)
        response = self.client.get(reverse('patient:update', args=[self.patient.id]))
        self.assertEqual(response.status_code, 403)
        response = self.client.get(reverse('patient:delete', args=[self.patient.id]))
        self.assertEqual(response.status_code, 403)

    def test_anonymous_access(self):
        response = self.client.get(reverse('patient:list'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
