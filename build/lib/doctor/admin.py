from django.contrib import admin
from .models import Doctor

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'specialization', 'phone', 'email', 'is_active', 'created_at')
    list_filter = ('specialization', 'is_active')
    search_fields = ('first_name', 'last_name', 'email')
    ordering = ('last_name', 'first_name')
