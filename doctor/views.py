from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django.urls import reverse_lazy
from .models import Doctor
from .forms import DoctorForm
from administrator.views_rbac import admin_required
from django.utils.decorators import method_decorator

class DoctorListView(ListView):
    model = Doctor
    template_name = 'doctor/list.html'
    context_object_name = 'doctors'
    
    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'profile') and user.profile.clinic:
            return Doctor.objects.filter(clinic=user.profile.clinic)
        else:
            return Doctor.objects.none()

@method_decorator(admin_required, name='dispatch')
class DoctorCreateView(CreateView):
    model = Doctor
    form_class = DoctorForm
    template_name = 'doctor/create.html'
    success_url = reverse_lazy('doctor:list')

class DoctorUpdateView(UpdateView):
    model = Doctor
    form_class = DoctorForm
    template_name = 'doctor/update.html'
    success_url = reverse_lazy('doctor:list')

class DoctorDetailView(DetailView):
    model = Doctor
    template_name = 'doctor/detail.html'
    context_object_name = 'doctor'

class DoctorDeleteView(DeleteView):
    model = Doctor
    template_name = 'doctor/delete.html'
    success_url = reverse_lazy('doctor:list')
