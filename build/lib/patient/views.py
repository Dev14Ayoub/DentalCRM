from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from .models import Patient
from .forms import PatientForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

class PatientListView(LoginRequiredMixin, ListView):
    model = Patient
    template_name = 'patient/list.html'
    context_object_name = 'patients'
    paginate_by = 10
    login_url = 'users:login'

    def get_queryset(self):
        return Patient.objects.filter(created_by=self.request.user).order_by('-created_at')

class PatientCreateView(LoginRequiredMixin, CreateView):
    model = Patient
    form_class = PatientForm
    template_name = 'patient/create.html'
    success_url = reverse_lazy('patient:list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, 'Patient created successfully!')
        return super().form_valid(form)

class PatientUpdateView(LoginRequiredMixin, UpdateView):
    model = Patient
    form_class = PatientForm
    template_name = 'patient/update.html'
    success_url = reverse_lazy('patient:list')

    def form_valid(self, form):
        messages.success(self.request, 'Patient updated successfully!')
        return super().form_valid(form)

class PatientDetailView(LoginRequiredMixin, DetailView):
    model = Patient
    template_name = 'patient/detail.html'
    context_object_name = 'patient'

class PatientDeleteView(LoginRequiredMixin, DeleteView):
    model = Patient
    template_name = 'patient/delete.html'
    success_url = reverse_lazy('patient:list')
    context_object_name = 'patient'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Patient deleted successfully!')
        return super().delete(request, *args, **kwargs)