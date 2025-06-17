from django.contrib import admin
from .models import Doctor
from django.utils.html import format_html

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('username', 'full_name', 'get_specialization_display', 'email', 'phone', 'profile_photo_display', 'is_active')
    search_fields = ('username', 'full_name', 'email', 'phone')
    list_filter = ('is_active', 'specialization')

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
