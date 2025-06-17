from django.contrib import admin
from .models import Task, Note, AppointmentReminder, OfficeAssistant
from django.utils.html import format_html

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'assigned_to', 'due_date', 'completed', 'created_at')
    list_filter = ('completed', 'due_date')
    search_fields = ('title', 'description')

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('created_by', 'created_at')
    search_fields = ('content',)

@admin.register(AppointmentReminder)
class AppointmentReminderAdmin(admin.ModelAdmin):
    list_display = ('user', 'appointment_date', 'reminder_sent')
    list_filter = ('reminder_sent',)

@admin.register(OfficeAssistant)
class OfficeAssistantAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email', 'phone_number', 'profile_photo_display')
    search_fields = ('username', 'first_name', 'last_name', 'email', 'phone_number')
    list_filter = ('first_name', 'last_name')

    def profile_photo_display(self, obj):
        if obj.profile_photo:
            return format_html('<img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 50%;" />', obj.profile_photo.url)
        return "-"
    profile_photo_display.short_description = 'Profile Photo'

    # Add password field to admin form
    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        if obj:
            fieldsets = list(fieldsets)
            fieldsets.append(('Password', {'fields': ('password',)}))
        return fieldsets

    # Allow admin to change password
    def save_model(self, request, obj, form, change):
        if 'password' in form.changed_data:
            obj.set_password(form.cleaned_data['password'])
        super().save_model(request, obj, form, change)
