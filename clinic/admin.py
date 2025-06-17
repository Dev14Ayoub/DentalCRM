from django.contrib import admin
from .models import Clinic
from doctor.models import Doctor
from patient.models import Patient

class DoctorInline(admin.TabularInline):
    model = Doctor
    extra = 0
    fields = ('first_name', 'last_name', 'specialization', 'phone', 'email', 'is_active')
    show_change_link = True

@admin.register(Clinic)
class ClinicAdmin(admin.ModelAdmin):
    list_display = ('name', 'monthly_income', 'annual_income')
    filter_horizontal = ('leads', 'doctors', 'patients')
    inlines = [DoctorInline]
