import string
import random
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from clinic.models import Clinic

def generate_special_id():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=10))

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20, blank=True)
    photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)
    special_id = models.CharField(max_length=10, unique=True, blank=True, null=True, editable=False)
    clinic = models.ForeignKey(Clinic, on_delete=models.SET_NULL, null=True, blank=True, related_name='administrators')

    def save(self, *args, **kwargs):
        if not self.special_id:
            unique = False
            while not unique:
                new_id = generate_special_id()
                if not Profile.objects.filter(special_id=new_id).exists():
                    self.special_id = new_id
                    unique = True
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Profile of {self.user.username}"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
