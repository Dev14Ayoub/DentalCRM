# dental/admin.py
from .models import Appointment
from django.contrib import admin 
@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'date_time', 'status')
    list_filter = ('status', 'date_time')
    search_fields = ('patient__name', 'purpose')
    date_hierarchy = 'date_time'