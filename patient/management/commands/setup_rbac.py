from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from patient.models import Patient
from doctor.models import Doctor
from office_assistant.models import OfficeAssistant
from leads.models import Lead

class Command(BaseCommand):
    help = 'Setup RBAC groups and permissions'

    def handle(self, *args, **options):
        # Clear existing groups
        Group.objects.all().delete()

        # Administrator group
        admin_group, created = Group.objects.get_or_create(name='Administrator')
        admin_permissions = Permission.objects.all()
        admin_group.permissions.set(admin_permissions)
        self.stdout.write(self.style.SUCCESS('Administrator group created with all permissions.'))

        # Doctor group
        doctor_group, created = Group.objects.get_or_create(name='Doctor')
        doctor_permissions = []
        # Add permissions for Doctor model
        doctor_ct = ContentType.objects.get_for_model(Doctor)
        doctor_permissions += Permission.objects.filter(content_type=doctor_ct)
        # Add permissions for Patient model (view, change)
        patient_ct = ContentType.objects.get_for_model(Patient)
        doctor_permissions += Permission.objects.filter(content_type=patient_ct, codename__in=['view_patient', 'change_patient'])
        # Add other relevant permissions as needed
        doctor_group.permissions.set(set(doctor_permissions))
        self.stdout.write(self.style.SUCCESS('Doctor group created with specific permissions.'))

        # Office Assistant group
        office_assistant_group, created = Group.objects.get_or_create(name='Office Assistant')
        office_assistant_permissions = []
        # Add permissions for OfficeAssistant model
        oa_ct = ContentType.objects.get_for_model(OfficeAssistant)
        office_assistant_permissions += Permission.objects.filter(content_type=oa_ct)
        # Add limited permissions for Patient and Appointment models
        office_assistant_permissions += Permission.objects.filter(content_type=patient_ct, codename__in=['view_patient', 'add_patient', 'change_patient'])
        # Add permissions for Appointment model (view, add, change, delete)
        appointment_ct = ContentType.objects.get(app_label='schedule', model='appointment')
        office_assistant_permissions += Permission.objects.filter(content_type=appointment_ct)
        office_assistant_group.permissions.set(set(office_assistant_permissions))
        self.stdout.write(self.style.SUCCESS('Office Assistant group created with specific permissions.'))

        # Lead group
        lead_group, created = Group.objects.get_or_create(name='Lead')
        lead_permissions = []
        lead_ct = ContentType.objects.get_for_model(Lead)
        lead_permissions += Permission.objects.filter(content_type=lead_ct)
        lead_group.permissions.set(set(lead_permissions))
        self.stdout.write(self.style.SUCCESS('Lead group created with specific permissions.'))

        self.stdout.write(self.style.SUCCESS('RBAC groups and permissions setup completed.'))
