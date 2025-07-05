from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, TemplateView
from django.urls import reverse_lazy
from .models import Appointment, DoctorAvailability, Notification
from administrator.models import AuditLog
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.conf import settings

class AppointmentListView(LoginRequiredMixin, ListView):
    model = Appointment
    template_name = 'calendar_app/appointment_list.html'
    context_object_name = 'appointments'

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'profile') and user.profile.clinic:
            return Appointment.objects.filter(clinic=user.profile.clinic)
        return Appointment.objects.none()

class AppointmentCreateView(LoginRequiredMixin, CreateView):
    model = Appointment
    fields = ['doctor', 'patient', 'start_time', 'end_time', 'notes']
    template_name = 'calendar_app/appointment_form.html'
    success_url = reverse_lazy('calendar_app:appointment_list')

    def form_valid(self, form):
        if hasattr(self.request.user, 'profile') and self.request.user.profile.clinic:
            form.instance.clinic = self.request.user.profile.clinic
        return super().form_valid(form)

class AppointmentUpdateView(LoginRequiredMixin, UpdateView):
    model = Appointment
    fields = ['doctor', 'patient', 'start_time', 'end_time', 'notes']
    template_name = 'calendar_app/appointment_form.html'
    success_url = reverse_lazy('calendar_app:appointment_list')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        user = self.request.user
        if not hasattr(user, 'profile') or not user.profile.clinic or obj.clinic != user.profile.clinic:
            from django.core.exceptions import PermissionDenied
            raise PermissionDenied("You do not have permission to edit this appointment.")
        return obj

    def form_valid(self, form):
        response = super().form_valid(form)
        # Create notification for appointment update
        Notification.objects.create(
            user=self.request.user,
            message=f"Appointment with {form.instance.patient} updated."
        )
        # Send email notification
        send_mail(
            subject='Appointment Updated',
            message=f'Your appointment with {form.instance.patient} has been updated.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[self.request.user.email],
            fail_silently=True,
        )
        # Audit log for appointment update
        AuditLog.objects.create(
            user=self.request.user,
            action_type='update_appointment',
            object_type='Appointment',
            object_id=form.instance.id,
            description=f"Updated appointment with patient {form.instance.patient}"
        )
        return response

class AppointmentDeleteView(LoginRequiredMixin, DeleteView):
    model = Appointment
    template_name = 'calendar_app/appointment_confirm_delete.html'
    success_url = reverse_lazy('calendar_app:appointment_list')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        user = self.request.user
        if not hasattr(user, 'profile') or not user.profile.clinic or obj.clinic != user.profile.clinic:
            from django.core.exceptions import PermissionDenied
            raise PermissionDenied("You do not have permission to delete this appointment.")
        return obj

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        response = super().delete(request, *args, **kwargs)
        # Audit log for appointment deletion
        AuditLog.objects.create(
            user=request.user,
            action_type='delete_appointment',
            object_type='Appointment',
            object_id=obj.id,
            description=f"Deleted appointment with patient {obj.patient}"
        )
        # Send email notification
        send_mail(
            subject='Appointment Deleted',
            message=f'Your appointment with {obj.patient} has been deleted.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[request.user.email],
            fail_silently=True,
        )
        return response

class DoctorAvailabilityListView(LoginRequiredMixin, ListView):
    model = DoctorAvailability
    template_name = 'calendar_app/doctoravailability_list.html'
    context_object_name = 'availabilities'

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'profile') and user.profile.clinic:
            return DoctorAvailability.objects.filter(clinic=user.profile.clinic)
        return DoctorAvailability.objects.none()

class DoctorAvailabilityCreateView(LoginRequiredMixin, CreateView):
    model = DoctorAvailability
    fields = ['doctor', 'start_time', 'end_time', 'is_vacation', 'reason']
    template_name = 'calendar_app/doctoravailability_form.html'
    success_url = reverse_lazy('calendar_app:doctoravailability_list')

    def form_valid(self, form):
        if hasattr(self.request.user, 'profile') and self.request.user.profile.clinic:
            form.instance.clinic = self.request.user.profile.clinic
        response = super().form_valid(form)
        # Create notification for doctor availability creation
        Notification.objects.create(
            user=self.request.user,
            message=f"Doctor availability for {form.instance.doctor} created."
        )
        return response

class DoctorAvailabilityUpdateView(LoginRequiredMixin, UpdateView):
    model = DoctorAvailability
    fields = ['doctor', 'start_time', 'end_time', 'is_vacation', 'reason']
    template_name = 'calendar_app/doctoravailability_form.html'
    success_url = reverse_lazy('calendar_app:doctoravailability_list')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        user = self.request.user
        if not hasattr(user, 'profile') or not user.profile.clinic or obj.clinic != user.profile.clinic:
            from django.core.exceptions import PermissionDenied
            raise PermissionDenied("You do not have permission to edit this doctor availability.")
        return obj

    def form_valid(self, form):
        response = super().form_valid(form)
        # Create notification for doctor availability update
        Notification.objects.create(
            user=self.request.user,
            message=f"Doctor availability for {form.instance.doctor} updated."
        )
        # Send email notification
        send_mail(
            subject='Doctor Availability Updated',
            message=f'Doctor availability for {form.instance.doctor} has been updated.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[self.request.user.email],
            fail_silently=True,
        )
        # Audit log for doctor availability update
        AuditLog.objects.create(
            user=self.request.user,
            action_type='update_doctor_availability',
            object_type='DoctorAvailability',
            object_id=form.instance.id,
            description=f"Updated doctor availability for {form.instance.doctor}"
        )
        return response

class DoctorAvailabilityDeleteView(LoginRequiredMixin, DeleteView):
    model = DoctorAvailability
    template_name = 'calendar_app/doctoravailability_confirm_delete.html'
    success_url = reverse_lazy('calendar_app:doctoravailability_list')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        user = self.request.user
        if not hasattr(user, 'profile') or not user.profile.clinic or obj.clinic != user.profile.clinic:
            from django.core.exceptions import PermissionDenied
            raise PermissionDenied("You do not have permission to delete this doctor availability.")
        return obj

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        doctor = obj.doctor
        response = super().delete(request, *args, **kwargs)
        # Create notification for doctor availability deletion
        Notification.objects.create(
            user=request.user,
            message=f"Doctor availability for {doctor} deleted."
        )
        # Send email notification
        send_mail(
            subject='Doctor Availability Deleted',
            message=f'Doctor availability for {doctor} has been deleted.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[request.user.email],
            fail_silently=True,
        )
        # Audit log for doctor availability deletion
        AuditLog.objects.create(
            user=request.user,
            action_type='delete_doctor_availability',
            object_type='DoctorAvailability',
            object_id=obj.id,
            description=f"Deleted doctor availability for {doctor}"
        )
        return response

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils.dateparse import parse_datetime
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json

class CalendarView(LoginRequiredMixin, TemplateView):
    template_name = 'calendar_app/calendar.html'

class CalendarEventsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        if not hasattr(user, 'profile') or not user.profile.clinic:
            return Response([])

        clinic = user.profile.clinic
        appointments = Appointment.objects.filter(clinic=clinic)
        availabilities = DoctorAvailability.objects.filter(clinic=clinic)

        events = []

        for appt in appointments:
            events.append({
                'id': f'appt-{appt.id}',
                'title': f'Appointment: {appt.patient}',
                'start': appt.start_time.isoformat(),
                'end': appt.end_time.isoformat(),
                'color': 'blue',
            })

        for avail in availabilities:
            title = 'Vacation' if avail.is_vacation else 'Unavailable'
            events.append({
                'id': f'avail-{avail.id}',
                'title': f'{title}: {avail.doctor}',
                'start': avail.start_time.isoformat(),
                'end': avail.end_time.isoformat(),
                'color': 'red',
            })

        return Response(events)

    @method_decorator(csrf_exempt)
    def post(self, request, event_id):
        user = request.user
        if not hasattr(user, 'profile') or not user.profile.clinic:
            return JsonResponse({'error': 'Unauthorized'}, status=403)

        data = json.loads(request.body)
        start_time = parse_datetime(data.get('start_time'))
        end_time = parse_datetime(data.get('end_time'))

        if event_id.startswith('appt-'):
            appt_id = int(event_id.split('-')[1])
            try:
                appt = Appointment.objects.get(id=appt_id, clinic=user.profile.clinic)

                # Conflict detection: check if new time overlaps with other appointments for the same doctor
                conflicts = Appointment.objects.filter(
                    doctor=appt.doctor,
                    clinic=user.profile.clinic,
                    start_time__lt=end_time,
                    end_time__gt=start_time
                ).exclude(id=appt.id)

                if conflicts.exists():
                    return JsonResponse({'error': 'Appointment time conflicts with existing appointment.'}, status=400)

                appt.start_time = start_time
                appt.end_time = end_time
                appt.save()
                return JsonResponse({'success': True})
            except Appointment.DoesNotExist:
                return JsonResponse({'error': 'Appointment not found'}, status=404)
        else:
            return JsonResponse({'error': 'Invalid event type'}, status=400)
