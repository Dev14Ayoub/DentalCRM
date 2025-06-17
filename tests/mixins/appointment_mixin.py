from schedule.models import Appointment, Procedure
from django.contrib.auth.models import User
from datetime import datetime, date, time


class AppointmentMixin:
    def make_user(self, username='user', password='pass'):
        user, created = User.objects.get_or_create(username=username)
        if created:
            user.set_password(password)
            user.save()
        return user

    def make_appointment(self, user_data=None, date_data=None, time_data=None):
        if user_data is None:
            user_data = self.make_user()
        if date_data is None:
            date_data = date.today()
        if time_data is None:
            time_data = time(hour=9, minute=0)
        procedure, _ = Procedure.objects.get_or_create(
            name='Test Procedure',
            defaults={
                'name_pt': 'Procedimento de Teste',
                'description': 'Test procedure description',
                'description_pt': 'Descrição do procedimento de teste',
                'price': 100.00,
            }
        )
        appointment = Appointment.objects.create(
            user=user_data,
            date=date_data,
            time=time_data,
            procedure=procedure,
        )
        return appointment

    def make_appointments_in_batch(self, user_data=None, datetime_list=None):
        if user_data is None:
            user_data = self.make_user()
        if datetime_list is None:
            datetime_list = [(date.today(), time(hour=9, minute=0))]
        appointments = []
        for dt in datetime_list:
            date_val, time_val = dt
            if not date_val:
                date_val = date.today()
            if not time_val:
                time_val = time(hour=9, minute=0)
            # Parse time_val if it is a string
            if isinstance(time_val, str):
                hour, minute = map(int, time_val.split(':'))
                time_val = time(hour=hour, minute=minute)
            appointment = self.make_appointment(
                user_data=user_data,
                date_data=date_val,
                time_data=time_val
            )
            appointments.append(appointment)
        return appointments
