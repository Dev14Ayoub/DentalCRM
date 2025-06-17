from django.contrib import admin
from .models import Lead

@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'phone', 'status', 'source', 'created_at')
    list_filter = ('status', 'source', 'created_at')
    search_fields = ('id', 'name', 'email', 'phone')
    readonly_fields = ('id', 'created_at', 'updated_at')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('ID Information', {
            'fields': ('id',),
            'classes': ('collapse',),
            'description': 'Automatically generated unique identifier'
        }),
        ('Contact Details', {
            'fields': ('name', 'email', 'phone')
        }),
        ('Status Information', {
            'fields': ('status', 'source')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
        ('Additional Notes', {
            'fields': ('notes',)
        }),
    )

    # To maintain clickable name instead of ID
    list_display_links = ('name',)