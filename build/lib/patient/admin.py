from django.contrib import admin
from .models import Patient

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email', 'phone', 'status', 'created_at')
    list_filter = ('status', 'gender', 'created_at')
    search_fields = ('id', 'first_name', 'last_name', 'email', 'phone')
    readonly_fields = ('id', 'created_at', 'updated_at')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('ID Information', {
            'fields': ('id',),
            'classes': ('collapse',),
            'description': 'Automatically generated unique identifier'
        }),
        ('Personal Details', {
            'fields': ('first_name', 'last_name', 'date_of_birth', 'gender')
        }),
        ('Contact Information', {
            'fields': ('email', 'phone', 'address')
        }),
        ('Medical Information', {
            'fields': ('medical_history',)
        }),
        ('Status Information', {
            'fields': ('status',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
        ('Created By', {
            'fields': ('created_by',),
            'classes': ('collapse',)
        }),
    )