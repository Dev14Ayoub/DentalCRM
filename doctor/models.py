from django.db import models
from django.utils.translation import gettext_lazy as _
class Doctor(models.Model):
    class Specialization(models.TextChoices):
        GENERAL_DENTIST = 'GD', _('General Dentist')
        ORTHODONTIST = 'OR', _('Orthodontist')
        PERIODONTIST = 'PE', _('Periodontist')
        ENDODONTIST = 'EN', _('Endodontist')
        ORAL_SURGEON = 'OS', _('Oral Surgeon')
        PEDIATRIC_DENTIST = 'PD', _('Pediatric Dentist')
        PROSTHODONTIST = 'PR', _('Prosthodontist')
    
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    username = models.CharField(max_length=150, unique=True, null=True, blank=True)
    specialization = models.CharField(
        max_length=2, 
        choices=Specialization.choices, 
        default=Specialization.GENERAL_DENTIST
    )
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    address = models.TextField(blank=True, null=True)
    clinic = models.ForeignKey('clinic.Clinic', on_delete=models.CASCADE, related_name='doctor_clinic', null=True, blank=True)
    profile_photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)
    password = models.CharField(max_length=128, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
