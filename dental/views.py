# dental/views.py
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from dental.models import Patient
from django.urls import reverse_lazy

from django.shortcuts import render


from django.db.models import Q
from django.views.generic import DetailView

from .models import Appointment

class PatientListView(LoginRequiredMixin, ListView):
    model = Patient
    template_name = 'dental/patient_list.html'
    context_object_name = 'patients'
    paginate_by = 9  # 3x3 grid

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('q')
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) | Q(phone__icontains=search_query) | Q(email__icontains=search_query)
            )
        return queryset.order_by('-registration_date')

class PatientDetailView(LoginRequiredMixin, DetailView):
    model = Patient
    template_name = 'dental/patient_detail.html'

class PatientCreateView(LoginRequiredMixin, CreateView):
    model = Patient
    fields = '__all__'
    template_name = 'dental/patient_form.html'
    success_url = reverse_lazy('patient_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)
    
def appointment_calendar(request):
    return render(request, 'dental/appointment_calendar.html')




class AppointmentListView(ListView):
    model = Appointment
    template_name = 'dental/appointment_list.html'
    context_object_name = 'appointments'
    paginate_by = 9

    def get_queryset(self):
        queryset = super().get_queryset().select_related('patient', 'doctor')
        status = self.request.GET.get('status')
        date = self.request.GET.get('date')

        if status:
            queryset = queryset.filter(status=status)
        if date:
            queryset = queryset.filter(date_time__date=date)
            
        return queryset.order_by('-date_time')

class AppointmentDetailView(LoginRequiredMixin, DetailView):
    model = Appointment
    template_name = 'dental/appointment_detail.html'
