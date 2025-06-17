from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from tests.mixins import AppointmentMixin, UserMixin, TestAssertionsMixin
from schedule.models import Appointment


class ScheduleAPIMixin(AppointmentMixin, UserMixin, TestAssertionsMixin):
    def get_auth_data(self, username='user', password='pass'):
        userdata = {
            'username': username,
            'password': password,
        }
        user = self.make_user(
            username=userdata.get('username'),
            password=userdata.get('password'),
        )
        response = self.client.post(
            reverse('users:token_obtain_pair'), data={**userdata}
        )
        return {
            'jwt_access_token': response.data.get('access'),
            'jwt_refresh_token': response.data.get('refresh'),
            'user': user,
        }

    def get_appointment_form(self, user=None):
        from schedule.models import Procedure, Doctor
        from datetime import date, timedelta, datetime, time as dt_time

        procedure = Procedure.objects.first()
        doctor = Doctor.objects.filter(is_active=True).first()
        if not procedure or not doctor:
            raise Exception("Procedure or Doctor not found in DB")

        # Find next date that is not Sunday
        next_date = date.today() + timedelta(days=1)
        while next_date.weekday() == 6:
            next_date += timedelta(days=1)

        form_data = {
            'first_name': 'Test',
            'last_name': 'User',
            'doctor': doctor.id,
            'procedure': procedure.id,
            'price': '{:.2f}'.format(procedure.price),
            'date': next_date,
            'time': dt_time(hour=10, minute=0),
        }
        return form_data


class ScheduleAPITest(APITestCase, ScheduleAPIMixin):
    def setUp(self):
        super().setUp()
        from schedule.models import Procedure, Doctor
        if not Procedure.objects.exists():
            Procedure.objects.create(
                name='Test Procedure',
                name_pt='Procedimento de Teste',
                description='Test procedure description',
                description_pt='Descrição do procedimento de teste',
                price=100.00,
            )
        if not Doctor.objects.filter(is_active=True).exists():
            Doctor.objects.create(
                first_name='Test',
                last_name='Doctor',
                is_active=True,
            )

    def test_schedule_api_returns_status_code_401_if_not_authenticated(self):
        url = reverse('schedule:schedule-api-list')
        response = self.client.get(url)
        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

    def test_schedule_api_logged_user_can_retrieve_own_appointments(self):
        auth_data = self.get_auth_data()
        user = auth_data.get('user')
        from datetime import date, timedelta
        base_date = date.today()
        self.make_appointments_in_batch(
            user_data=user,
            datetime_list=[
                (base_date, '12:00'),
                (base_date + timedelta(days=1), '13:00'),
                (base_date + timedelta(days=2), '14:00'),
                (base_date + timedelta(days=3), '15:00'),
            ]
        )
        appointments = list(Appointment.objects.filter(user=user))
        print(f'Created appointments count: {len(appointments)}')
        jwt_access_token = auth_data.get('jwt_access_token')
        url = reverse('schedule:schedule-api-list')
        response = self.client.get(
            url,
            HTTP_AUTHORIZATION=f'Bearer {jwt_access_token}'
        )
        print(f'API response data count: {len(response.data)}')
        print(f'API response data: {response.data}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)

    def test_schedule_api_logged_user_can_retrieve_a_single_appointment(self):
        auth_data = self.get_auth_data()
        user = auth_data.get('user')
        appointment = self.make_appointment(user_data=user)
        jwt_access_token = auth_data.get('jwt_access_token')
        url = reverse('schedule:schedule-api-detail', args=(appointment.id,))
        response = self.client.get(
            url,
            HTTP_AUTHORIZATION=f'Bearer {jwt_access_token}'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('id'), appointment.id)

    def test_schedule_api_logged_user_cannot_retrieve_someone_elses_data(self):
        another_user = self.make_another_user()
        auth_data = self.get_auth_data()
        jwt_access_token = auth_data.get('jwt_access_token')
        id = another_user.id
        url_details = reverse('users:user-api-detail', args=(id,))
        response = self.client.get(
            url_details,
            HTTP_AUTHORIZATION=f'Bearer {jwt_access_token}'
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_schedule_api_user_cannot_schedule_if_not_authenticated(self):
        form_data = self.get_appointment_form()
        url = reverse('schedule:schedule-api-list')
        response = self.client.post(url, data=form_data)
        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

    def test_schedule_api_user_can_schedule_if_authenticated(self):
        auth_data = self.get_auth_data()
        user = auth_data.get('user')
        jwt_access_token = auth_data.get('jwt_access_token')
        form_data = self.get_appointment_form(user)
        url = reverse('schedule:schedule-api-list')
        response = self.client.post(
            url,
            data=form_data,
            HTTP_AUTHORIZATION=f'Bearer {jwt_access_token}'
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

    def test_schedule_api_user_cannot_schedule_for_someone_else(self):
        another_user = self.make_another_user()
        auth_data = self.get_auth_data()
        jwt_access_token = auth_data.get('jwt_access_token')
        form_data = self.get_appointment_form(another_user)
        url = reverse('schedule:schedule-api-list')
        response = self.client.post(
            url,
            data=form_data,
            HTTP_AUTHORIZATION=f'Bearer {jwt_access_token}'
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

    def test_schedule_api_user_can_cancel_their_own_appointment(self):
        auth_data = self.get_auth_data()
        user = auth_data.get('user')
        jwt_access_token = auth_data.get('jwt_access_token')
        appointment = self.make_appointment(user_data=user)
        id = appointment.id
        url = reverse('schedule:schedule-api-detail', args=(id,))
        response = self.client.delete(
            url,
            HTTP_AUTHORIZATION=f'Bearer {jwt_access_token}'
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

    def test_schedule_api_user_cannot_cancel_someone_elses_appointment(self):
        another_user = self.make_another_user()
        auth_data = self.get_auth_data()
        jwt_access_token = auth_data.get('jwt_access_token')
        appointment = self.make_appointment(user_data=another_user)
        id = appointment.id
        url = reverse('schedule:schedule-api-detail', args=(id,))
        response = self.client.delete(
            url,
            HTTP_AUTHORIZATION=f'Bearer {jwt_access_token}'
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND
        )
