# dental/models.py
from django.db import models
from django.urls import reverse
from datetime import date

from django.contrib.gis.db import models as gis_models
from phonenumber_field.modelfields import PhoneNumberField

from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class Patient(models.Model):
    GENDER_CHOICES = [('M', 'Male'), ('F', 'Female'), ('O', 'Other')]
    
    name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    phone = PhoneNumberField()
    email = models.EmailField(blank=True)
    medical_history = models.TextField(blank=True)
    registration_date = models.DateTimeField(auto_now_add=True)
    profile_picture = models.ImageField(upload_to='patients/', blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('patient_detail', kwargs={'pk': self.pk})
    
    @property
    def age(self):
        today = date.today()
        return today.year - self.date_of_birth.year - (
            (today.month, today.day) < 
            (self.date_of_birth.month, self.date_of_birth.day)
        )
    
    @property
    def upcoming_appointments(self):
        return self.appointments.filter(
            date_time__gte=timezone.now(),
            status='SCH'
        ).order_by('date_time')


class Doctor(models.Model):
    SPECIALIZATION_CHOICES = [
        ('GEN', 'General Dentistry'),
        ('ORT', 'Orthodontics'),
        ('PED', 'Pediatric Dentistry'),
        ('PER', 'Periodontics'),
        ('SUR', 'Oral Surgery'),
    ]
    
    user = models.OneToOneField(
        'auth.User',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='doctor_profile'
    )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    specialization = models.CharField(max_length=3, choices=SPECIALIZATION_CHOICES)
    license_number = models.CharField(max_length=20, unique=True)
    phone = PhoneNumberField(region='US')
    email = models.EmailField()
    office_hours = models.JSONField(  # Store as {"monday": ["09:00", "17:00"], ...}
        default=dict,
        blank=True
    )
    profile_picture = models.ImageField(
        upload_to='doctors/',
        blank=True,
        null=True
    )
    bio = models.TextField(blank=True)
    office_location = gis_models.PointField(  # Requires GeoDjango setup
        srid=4326,
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['last_name', 'first_name']
        verbose_name = 'Dental Professional'

    def __str__(self):
        return f"Dr. {self.last_name}, {self.specialization}"

    def get_absolute_url(self):
        return reverse('doctor_detail', kwargs={'pk': self.pk})

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('SCH', 'Scheduled'),
        ('COM', 'Completed'),
        ('CAN', 'Canceled'),
        ('RES', 'Rescheduled'),
    ]
    
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='appointments'
    )
    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.SET_NULL,
        null=True,
        related_name='appointments'
    )
    date_time = models.DateTimeField()
    duration = models.PositiveIntegerField(  # In minutes
        default=30,
        help_text="Appointment duration in minutes"
    )
    purpose = models.CharField(max_length=200)
    status = models.CharField(
        max_length=3,
        choices=STATUS_CHOICES,
        default='SCH'
    )
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date_time']
        indexes = [
            models.Index(fields=['date_time']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return f"{self.patient.name} - {self.date_time.strftime('%b %d, %Y %I:%M %p')}"

    def get_status_color(self):
        return {
            'SCH': 'info',
            'COM': 'success',
            'CAN': 'danger',
            'RES': 'warning'
        }.get(self.status, 'secondary')

class Treatment(models.Model):
    TREATMENT_TYPES = [
        ('FILL', 'Filling'),
        ('CLEAN', 'Cleaning'),
        ('ROOT', 'Root Canal'),
        ('BRACE', 'Braces Adjustment'),
        ('EXAM', 'Examination'),
    ]
    
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='treatments'
    )
    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.SET_NULL,
        null=True,
        related_name='treatments'
    )
    treatment_type = models.CharField(
        max_length=5,
        choices=TREATMENT_TYPES
    )
    date = models.DateField()
    description = models.TextField()
    cost = models.DecimalField(
        max_digits=8,
        decimal_places=2
    )
    insurance_covered = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0
    )
    follow_up_required = models.BooleanField(default=False)
    follow_up_date = models.DateField(blank=True, null=True)
    documents = models.ManyToManyField(
        'MedicalDocument',
        blank=True,
        related_name='treatments'
    )

    class Meta:
        ordering = ['-date']
        verbose_name = 'Treatment Record'

    def __str__(self):
        return f"{self.get_treatment_type_display()} - {self.patient.name}"

class MedicalDocument(models.Model):
    DOCUMENT_TYPES = [
        ('XRAY', 'X-Ray Image'),
        ('SCRIPT', 'Prescription'),
        ('REPORT', 'Medical Report'),
        ('BILL', 'Invoice/Bill'),
        ('OTHER', 'Other'),
    ]
    
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='documents'
    )
    title = models.CharField(max_length=200)
    document_type = models.CharField(
        max_length=6,
        choices=DOCUMENT_TYPES,
        default='OTHER'
    )
    file = models.FileField(
        upload_to='medical_documents/%Y/%m/%d/',
        max_length=500
    )
    upload_date = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True)
    related_appointment = models.ForeignKey(
        Appointment,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='documents'
    )

    class Meta:
        ordering = ['-upload_date']

    def __str__(self):
        return f"{self.title} - {self.patient.name}"

    def file_extension(self):
        return self.file.name.split('.')[-1].upper()
    



class Appointment(models.Model):
    STATUS_CHOICES = [
        ('SCH', 'Scheduled'),
        ('COM', 'Completed'),
        ('CAN', 'Cancelled'),
        ('RES', 'Rescheduled'),
    ]

    patient = models.ForeignKey(
        'Patient',
        on_delete=models.CASCADE,
        related_name='appointments'
    )
    doctor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'groups__name': 'Doctors'}
    )
    date_time = models.DateTimeField(default=timezone.now)
    duration = models.PositiveIntegerField(
        default=30,
        help_text="Duration in minutes"
    )
    purpose = models.CharField(max_length=200)
    status = models.CharField(
        max_length=3,
        choices=STATUS_CHOICES,
        default='SCH'
    )
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date_time']
        verbose_name = 'Appointment'
        verbose_name_plural = 'Appointments'

    def __str__(self):
        return f"{self.patient.name} - {self.date_time.strftime('%b %d, %Y %I:%M %p')}"

    def get_status_color(self):
        status_colors = {
            'SCH': 'info',
            'COM': 'success',
            'CAN': 'danger',
            'RES': 'warning'
        }
        return status_colors.get(self.status, 'secondary')