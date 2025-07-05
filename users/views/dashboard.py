from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.translation import gettext as _
from django.views import View
from django.views.generic import DetailView

from schedule.models import Appointment


class UserDashboardView(LoginRequiredMixin, View):
    login_url = 'users:login'
    redirect_field_name = 'next'

    def get_appointment(self, id=None):
        appointment = None
        if id:
            appointment = Appointment.objects.filter(
                is_completed=False,
                user=self.request.user,
                id=id,
            ).first()
            if not appointment:
                raise Http404()
        return appointment

    def get(self, request):
        from administrator.models import UserRole, Role
        user_roles = UserRole.objects.filter(user=request.user).select_related('role')
        roles = [ur.role.name for ur in user_roles]

        appointments = Appointment.objects.select_related('user', 'procedure').filter(is_completed=False)
        closed_appointments = Appointment.objects.select_related('user', 'procedure').filter(is_completed=True)

        if 'Doctor' in roles:
            # Doctors should see appointments for their clinic
            if hasattr(request.user, 'profile') and request.user.profile.clinic:
                appointments = appointments.filter(user__profile__clinic=request.user.profile.clinic)
                closed_appointments = closed_appointments.filter(user__profile__clinic=request.user.profile.clinic)
            else:
                appointments = appointments.none()
                closed_appointments = closed_appointments.none()
        elif 'Office Assistant' in roles:
            # Filter appointments for office assistant's clinic
            if hasattr(request.user, 'profile') and request.user.profile.clinic:
                appointments = appointments.filter(user__profile__clinic=request.user.profile.clinic)
                closed_appointments = closed_appointments.filter(user__profile__clinic=request.user.profile.clinic)
        elif 'Administrator' in roles:
            # Administrator sees appointments for their clinic
            if hasattr(request.user, 'profile') and request.user.profile.clinic:
                appointments = appointments.filter(user__profile__clinic=request.user.profile.clinic)
                closed_appointments = closed_appointments.filter(user__profile__clinic=request.user.profile.clinic)
            else:
                # If no clinic, show all
                pass
        else:
            # Default: show only user's own appointments
            appointments = appointments.filter(user=request.user)
            closed_appointments = closed_appointments.filter(user=request.user)

        appointments = appointments.order_by('date', 'time')
        closed_appointments = closed_appointments.order_by('date', 'time')

        context = {
            'appointments': appointments,
            'closed_appointments': closed_appointments,
            'show_full_name': True,
        }
        return render(request, 'users/pages/dashboard.html', context=context)


@method_decorator(
    login_required(login_url='users:login', redirect_field_name='next'),
    name='dispatch'
)
class DashboardAppointmentDelete(UserDashboardView):
    def post(self, *args, **kwargs):
        appointment = self.get_appointment(self.request.POST.get('id'))
        appointment.delete()
        messages.success(self.request, _('Appointment successfully canceled'))
        return redirect(reverse('users:dashboard'))


class AppointmentDetailView(DetailView):
    model = Appointment
    context_object_name = 'appointment'
    template_name = 'users/pages/appointment.html'

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(user=self.request.user)
        return queryset
