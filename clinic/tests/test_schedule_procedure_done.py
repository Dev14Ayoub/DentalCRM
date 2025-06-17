import pytest
from django.urls import reverse
from django.test import Client
from schedule.models import Appointment, Procedure
from patient.models import Patient
from doctor.models import Doctor
from clinic.models import Clinic

@pytest.mark.django_db
def test_mark_procedure_done(db, django_user_model):
    clinic = Clinic.objects.create(name="Test Clinic")
    doctor = Doctor.objects.create(first_name="Dr.", last_name="Smith", clinic=clinic)
    user = django_user_model.objects.create_user(username='testuser', password='password')
    patient = Patient.objects.create(first_name="Patient", last_name="One", date_of_birth="1990-01-01", gender="M", phone="1234567890", created_by=user, clinic=clinic)

    procedure = Procedure.objects.create(name="Procedure One", name_pt="Procedimento Um", description="Desc", description_pt="Descrição", price=100)
    appointment = Appointment.objects.create(user=user, doctor=doctor, procedure=procedure, date="2025-01-01", time="10:00", is_completed=False)

    client = Client()
    client.login(username='testuser', password='password')
    url = reverse('schedule:mark_procedure_done', args=[appointment.id])
    response = client.post(url)

    assert response.status_code == 302
    appointment.refresh_from_db()
    assert appointment.is_completed is True

@pytest.mark.django_db
def test_schedule_list_view_contains_procedure_done_button(db, django_user_model):
    user = django_user_model.objects.create_user(username='testuser2', password='password')
    clinic = Clinic.objects.create(name="Test Clinic")
    doctor = Doctor.objects.create(first_name="Dr.", last_name="Smith", clinic=clinic)
    patient = Patient.objects.create(first_name="Patient", last_name="One", date_of_birth="1990-01-01", gender="M", phone="1234567890", created_by=user, clinic=clinic)
    procedure = Procedure.objects.create(name="Procedure One", name_pt="Procedimento Um", description="Desc", description_pt="Descrição", price=100)
    appointment = Appointment.objects.create(user=user, doctor=doctor, procedure=procedure, date="2025-01-01", time="10:00", is_completed=False)

    client = Client()
    client.force_login(user)
    client.get('/')  # Load session
    url = reverse('schedule:schedule')
    response = client.get(url, follow=True)
    with open('test_schedule_page.html', 'w', encoding='utf-8') as f:
        f.write(response.content.decode())
    assert response.status_code == 200
    assert response.context['user'].is_authenticated
    assert 'schedule/pages/schedule.html' in [t.name for t in response.templates]
    assert b'Mark as Done' in response.content
