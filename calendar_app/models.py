from django.db import models
from django.conf import settings
from clinic.models import Clinic
from doctor.models import Doctor
from patient.models import Patient

class Appointment(models.Model):
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    notes = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['start_time']

    def __str__(self):
        return f"Appointment with Dr. {self.doctor} for {self.patient} on {self.start_time}"

class DoctorAvailability(models.Model):
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_vacation = models.BooleanField(default=False)
    reason = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        ordering = ['start_time']

    def __str__(self):
        status = "Vacation" if self.is_vacation else "Unavailable"
        return f"{status} for Dr. {self.doctor} from {self.start_time} to {self.end_time}"

class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.user.username} at {self.created_at}"
