from django.shortcuts import render
from django.views import View
from .models import Clinic

class ClinicListView(View):
    def get(self, request):
        clinics = Clinic.objects.all()
        context = {
            'clinics': clinics,
        }
        return render(request, 'clinic/clinic_list.html', context)
