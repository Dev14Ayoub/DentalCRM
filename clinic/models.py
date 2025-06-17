from django.db import models
from leads.models import Lead
from doctor.models import Doctor
from patient.models import Patient

class Clinic(models.Model):
    name = models.CharField(max_length=255)
    leads = models.ManyToManyField(Lead, related_name='clinics', blank=True)
    doctors = models.ManyToManyField(Doctor, related_name='clinics', blank=True)
    patients = models.ManyToManyField(Patient, related_name='clinics', blank=True)
    monthly_income = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    annual_income = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return self.name
