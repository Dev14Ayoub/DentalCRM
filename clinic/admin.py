from django.contrib import admin
from .models import Clinic
from doctor.models import Doctor
from patient.models import Patient
from users.models import Profile

class DoctorInline(admin.TabularInline):
    model = Doctor
    extra = 0
    fields = ('first_name', 'last_name', 'specialization', 'phone', 'email', 'is_active')
    show_change_link = True

class ProfileInline(admin.TabularInline):
    model = Profile
    extra = 0
    fields = ('user', 'phone_number', 'photo')
    readonly_fields = ('user',)
    can_delete = False
    verbose_name = 'Administrator'
    verbose_name_plural = 'Administrators'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Filter profiles linked to the current clinic
        return qs.filter(clinic__isnull=False)

@admin.register(Clinic)
class ClinicAdmin(admin.ModelAdmin):
    list_display = ('name', 'monthly_income', 'annual_income')
    filter_horizontal = ('leads', 'doctors', 'patients')
    inlines = [DoctorInline, ProfileInline]
