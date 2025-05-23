# dental/views.py
from django.views.generic import ListView, DetailView, CreateView
from dental.models import Patient
from django.urls import reverse_lazy

from django.shortcuts import render


from django.db.models import Q

class PatientListView(ListView):
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

class PatientDetailView(DetailView):
    model = Patient
    template_name = 'dental/patient_detail.html'

class PatientCreateView(CreateView):
    model = Patient
    fields = '__all__'
    template_name = 'dental/patient_form.html'
    success_url = reverse_lazy('patient_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)
    
def appointment_calendar(request):
    return render(request, 'dental/appointment_calendar.html')