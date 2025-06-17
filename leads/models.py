from django.db import models
import uuid
from django_currentuser.middleware import get_current_authenticated_user

def generate_lead_id():
    """Generate 12-character uppercase alphanumeric ID"""
    return uuid.uuid4().hex[:12].upper()

class Lead(models.Model):
    STATUS_CHOICES = [
        ('new', 'New'),
        ('contacted', 'Contacted'),
        ('converted', 'Converted'),
        ('lost', 'Lost'),
    ]
    
    SOURCE_CHOICES = [
        ('website', 'Website'),
        ('phone', 'Phone'),
        ('referral', 'Referral'),
        ('social', 'Social Media'),
    ]

    id = models.CharField(
        primary_key=True,
        max_length=12,
        default=generate_lead_id,
        editable=False,
        unique=True
    )
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    source = models.CharField(max_length=20, choices=SOURCE_CHOICES, default='website')
    notes = models.TextField(blank=True)
    clinic = models.ForeignKey('clinic.Clinic', on_delete=models.CASCADE, related_name='lead_clinic', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.clinic:
            user = get_current_authenticated_user()
            if user and hasattr(user, 'profile') and user.profile.clinic:
                self.clinic = user.profile.clinic
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.id} - {self.name} - {self.get_status_display()}"
    
    
    def convert(self):
        """Mark lead as converted"""
        if self.status != 'converted':
            self.status = 'converted'
            self.save()
            return True
        return False
