import datetime as dt

from django.http import JsonResponse, HttpResponseForbidden
from django.urls import reverse
from django.views import View
from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator

from schedule.models import Appointment


class AvailableAppointmentTimes(View):
    def get(self, request):
        selected_date = request.GET.get('date')
        if not selected_date:
            return JsonResponse({'error': 'Missing required parameter: date'}, status=400)
        booked_appointments = Appointment.objects.filter(
            date=selected_date).values_list('time', flat=True)
        booked_appointments = [apt.strftime('%H:%M')
                               for apt in booked_appointments]
        all_times = [f'{i:02d}:00' for i in range(8, 18)]
        available_times = [
            time for time in all_times if time not in booked_appointments
        ]
        return JsonResponse({'available_times': available_times})

    def get_url(self):
        return reverse('schedule:times')


class AvailableAppointmentDates(View):
    def get(self, request):
        selected_time = request.GET.get('time')
        booked_appointments = Appointment.objects.filter(
            time=selected_time).values_list('date', flat=True)
        today = dt.date.today()
        all_dates = [
            d.isoformat() for i in range(1, 61)
            if (d := (today + dt.timedelta(days=i))).weekday() != 6
        ]
        available_dates = [
            (date, dt.datetime.strptime(date, '%Y-%m-%d').strftime('%d-%m-%Y'))
            for date in all_dates if date not in booked_appointments
        ]
        return JsonResponse({'available_dates': available_dates})

    def get_url(self):
        return reverse('schedule:dates')


@method_decorator(permission_required('schedule.change_appointment', raise_exception=True), name='dispatch')
class ToggleAppointmentConfirmation(View):
    def post(self, request, pk):
        try:
            appointment = Appointment.objects.get(pk=pk)
        except Appointment.DoesNotExist:
            return JsonResponse({'error': 'Appointment not found'}, status=404)

        appointment.is_confirmed = not appointment.is_confirmed
        appointment.save()
        return JsonResponse({'success': True, 'is_confirmed': appointment.is_confirmed})

