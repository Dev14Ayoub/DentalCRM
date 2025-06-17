import datetime as dt

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import translation

from schedule.forms.appointment_form import AppointmentForm
from tests.mixins import AppointmentMixin


class AppointmentFormTest(TestCase, AppointmentMixin):
    @property
    def today(self):
        return dt.date.today()

    def setUp(self):
        super().setUp()
        self.appointment = self.make_appointment()
        self.user = self.appointment.user  # Add this line to set self.user

    def test_user_can_schedule_if_date_and_time_are_available(self):
        import datetime as dt
        with translation.override('en'):
            form = AppointmentForm(user=self.user)
            valid_date_str = form.fields['date'].widget.choices[0][0] if form.fields['date'].widget.choices else self.appointment.date
            valid_date = dt.date.fromisoformat(valid_date_str) if isinstance(valid_date_str, str) else valid_date_str
            valid_time_str = form.fields['time'].widget.choices[0][0] if form.fields['time'].widget.choices else self.appointment.time.strftime('%H:%M')
            valid_time = dt.datetime.strptime(valid_time_str, '%H:%M').time()
            form_data = {
                'procedure': self.appointment.procedure.id,
                'date': valid_date,
                'time': valid_time,
                'first_name': 'Test',
                'last_name': 'User',
            }
            form = AppointmentForm(data=form_data, user=self.user)
            if not form.is_valid():
                print("Form errors:", form.errors)
            self.assertTrue(form.is_valid())
            self.assertNotIn('date', form.errors)
            self.assertNotIn('time', form.errors)

    def test_user_cannot_schedule_if_date_and_time_are_not_available(self):
        with translation.override('en'):
            form_data = {
                'procedure': self.appointment.procedure.id,
                'date': self.appointment.date,
                'time': self.appointment.time.strftime('%H:%M'),
            }
            form = AppointmentForm(data=form_data, user=self.user)
            self.assertFalse(form.is_valid())
            self.assertIn('An appointment at this date and time has '
                          'already been booked by you!',
                          form.errors['date'])
            self.assertIn('An appointment at this date and time has '
                          'already been booked by you!',
                          form.errors['time'])

    def test_user_cannot_schedule_an_appointment_for_sunday(self):
        with translation.override('en'):
            for i in range(1, 8):
                next_sunday = self.today + dt.timedelta(days=i)
                if next_sunday.weekday() == 6:
                    break
            form_data = {
                'procedure': self.appointment.procedure.id,
                'date': next_sunday,
                'time': '13:00',
            }
            form = AppointmentForm(data=form_data)
            self.assertFalse(form.is_valid())
            self.assertIn('Invalid date selected.',
                          form.errors['date'])

    def test_user_cannot_schedule_an_appointment_out_of_time_range(self):
        with translation.override('en'):
            for i in range(1, 8):
                next_monday = self.today + dt.timedelta(days=i)
                if next_monday.weekday() == 0:
                    break
            form_data = {
                'procedure': self.appointment.procedure.id,
                'date': next_monday,
                'time': '23:00',
            }
            form = AppointmentForm(data=form_data)
            self.assertFalse(form.is_valid())
            self.assertIn('Invalid time selected.',
                          form.errors['time'])

    def test_user_is_redirected_to_dashboard_after_scheduling(self):
        import datetime as dt
        url = reverse('schedule:schedule')
        with translation.override('en'):
            user = User.objects.create_user(username='my_user', password='my_pass')
            self.client.login(username='my_user', password='my_pass')
            form = AppointmentForm(user=user)
            valid_date_str = form.fields['date'].widget.choices[0][0] if form.fields['date'].widget.choices else self.appointment.date
            valid_date = dt.date.fromisoformat(valid_date_str) if isinstance(valid_date_str, str) else valid_date_str
            valid_time_str = form.fields['time'].widget.choices[0][0] if form.fields['time'].widget.choices else self.appointment.time.strftime('%H:%M')
            valid_time = dt.datetime.strptime(valid_time_str, '%H:%M').time()
            form_data = {
                'procedure': self.appointment.procedure.id,
                'date': valid_date,
                'time': valid_time,
                'first_name': 'Test',
                'last_name': 'User',
            }
            response = self.client.post(url, data=form_data, follow=True)
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(
                response, 'users/pages/dashboard.html')
