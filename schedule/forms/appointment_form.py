import datetime as dt
from collections import defaultdict

from django import forms
from django.core.exceptions import ValidationError
from django.http import Http404
from django.utils.translation import gettext_lazy as _

from schedule.models import Appointment, Procedure
from schedule.validators import AppointmentValidator
from doctor.models import Doctor


class AppointmentForm(forms.ModelForm):
    first_name = forms.CharField(
        label=_('First Name'),
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': _('First Name')}),
    )
    last_name = forms.CharField(
        label=_('Last Name'),
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': _('Last Name')}),
    )
    price = forms.CharField(
        label=_('Price'),
        required=False,
        widget=forms.TextInput(attrs={'readonly': True, 'id': 'price'}),
    )

    def __init__(self, *args, user=None, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
        self._my_errors = defaultdict(lambda: [])
        self.fields['procedure'].widget.choices = [
            (p.pk, p) for p in Procedure.objects.all()
        ]
        today = dt.date.today()
        initial_times = []
        date_choices = [
            (today + dt.timedelta(days=i)).isoformat() for i in range(1, 61)
        ]
        first_procedure = Procedure.objects.first()
        price_str = '{:,.2f}'.format(
            first_procedure.price if first_procedure else 99.99
        ).replace('.', ',')
        self.fields['procedure'].initial = (first_procedure.id
                                            if first_procedure else 1)
        self.fields['procedure'].label = _('Procedure')
        self.fields['price'].initial = f'R$ {price_str}'
        for d, date_choice in enumerate(date_choices):
            if dt.date.fromisoformat(date_choice).weekday() == 6:
                continue
            unavailable_times = Appointment.objects.filter(
                date=date_choice).values_list('time', flat=True)
            unavailable_times = {t.strftime('%H:%M')
                                 for t in unavailable_times}
            time_choices = [
                (f'{i:02d}:00', f'{i:02d}:00') for i in range(8, 18)
                if f'{i:02d}:00' not in unavailable_times
            ]
            if time_choices:
                initial_times = time_choices[:]
                date_choices = date_choices[d:]
                break
        else:
            raise Http404(
                _('Sorry, we currently have no '
                  'available times for any dates soon.')
            )
        date_choices = [
            (date_choice, dt.datetime.strptime(
                date_choice, '%Y-%m-%d').strftime('%d-%m-%Y'))
            for date_choice in date_choices
            if dt.date.fromisoformat(date_choice).weekday() != 6
        ]
        self.fields['date'].widget.choices = date_choices
        self.fields['time'].widget.choices = initial_times or time_choices

        # Add doctor field with active doctors only
        self.fields['doctor'].queryset = Doctor.objects.filter(is_active=True)

    class Meta:
        model = Appointment
        fields = ('first_name', 'last_name', 'doctor', 'procedure', 'price', 'date', 'time')
        widgets = {
            'procedure': forms.Select(attrs={
                'id': 'procedure',
            }),
            'date': forms.Select,
            'time': forms.Select,
        }

    def clean(self):

        cleaned_data = super().clean()
        AppointmentValidator(
            cleaned_data, user=self.user, ErrorClass=ValidationError
        )
        return cleaned_data
