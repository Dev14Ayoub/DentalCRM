from django.contrib.auth.models import User
from users.forms.register_form import RegisterForm
from schedule.forms.appointment_form import AppointmentForm
from datetime import date

from schedule.models import Procedure

class UserMixin:
    def make_another_user(self, username='anotheruser', password='pass'):
        user, created = User.objects.get_or_create(username=username)
        if created:
            user.set_password(password)
            user.save()
        return user

    def get_appointment_form(self, user=None):
        if user is None:
            user = self.make_another_user()
        procedure, _ = Procedure.objects.get_or_create(
            name='Test Procedure',
            defaults={
                'name_pt': 'Procedimento de Teste',
                'description': 'Test procedure description',
                'description_pt': 'Descrição do procedimento de teste',
                'price': 100.00,
            }
        )
        form_data = {
            'date': date.today().strftime('%Y-%m-%d'),
            'time': '10:00',
            'procedure': procedure.id,
            'user': user.id,
        }
        # Return form data dict instead of form instance
        return form_data

    @property
    def today(self):
        return date.today()
