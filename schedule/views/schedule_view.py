from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views import View

from schedule.forms.appointment_form import AppointmentForm
from utils.send_email import send_confirmation


from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views import View

from schedule.forms.appointment_form import AppointmentForm
from utils.send_email import send_confirmation
from schedule.models import Appointment

class ScheduleView(View):
    template_name = 'schedule/pages/schedule.html'

    def get(self, request):
        import logging
        logger = logging.getLogger(__name__)
        form = AppointmentForm()
        curr_path = request.path
        appointments = Appointment.objects.filter(user=request.user).order_by('-date', '-time') if request.user.is_authenticated else []
        if hasattr(appointments, 'count') and callable(getattr(appointments, 'count')):
            # Defensive: appointments might be a list, so check type before calling count()
            if isinstance(appointments, list):
                count = len(appointments)
            else:
                count = appointments.count()
        elif isinstance(appointments, list):
            count = len(appointments)
        else:
            count = 0
        logger.debug(f"User: {request.user}, Appointments count: {count}")
        context = {
            'curr_path': curr_path,
            'form': form,
            'appointments': appointments,
        }
        response = render(
            self.request,
            self.template_name,
            context
        )
        logger.debug(f"Rendered template: {self.template_name} for user: {request.user}")
        return response

    def post(self, request):
        form = AppointmentForm(request.POST or None, user=request.user)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.user = request.user
            appointment.first_name = form.cleaned_data.get('first_name')
            appointment.last_name = form.cleaned_data.get('last_name')
            appointment.is_confirmed = False
            appointment.is_completed = False
            appointment.save()
            messages.success(
                request,
                _('Thank you for scheduling your appointment! You will '
                  'receive an email shortly to confirm your '
                  'appointment details.')
            )
            current_site = get_current_site(request)
            send_confirmation(appointment, current_site.domain)
            return redirect(reverse('users:dashboard'))
        messages.error(request, _('Failed to book your appointment!'))
        context = {
            'schedule_failed': True,
        }
        return render(self.request, self.template_name, context=context)

class MarkProcedureDoneView(View):
    def post(self, request, appointment_id):
        appointment = get_object_or_404(Appointment, id=appointment_id, user=request.user)
        appointment.is_completed = True
        appointment.save()
        messages.success(request, _('Procedure marked as done.'))
        return redirect(reverse('schedule:schedule'))
