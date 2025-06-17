from django.db import models
from django.contrib.auth.models import User
from django_currentuser.middleware import get_current_authenticated_user

class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Note(models.Model):
    content = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Note by {self.created_by} on {self.created_at}"

class AppointmentReminder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    appointment_date = models.DateTimeField()
    reminder_sent = models.BooleanField(default=False)

    def __str__(self):
        return f"Reminder for {self.user} on {self.appointment_date}"

class OfficeAssistant(models.Model):
    username = models.CharField(max_length=150, unique=True, null=True, blank=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    profile_photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)
    password = models.CharField(max_length=128)
    clinic = models.ForeignKey('clinic.Clinic', on_delete=models.CASCADE, related_name='office_assistant_clinic', null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.clinic:
            user = get_current_authenticated_user()
            if user and hasattr(user, 'profile') and user.profile.clinic:
                self.clinic = user.profile.clinic
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
