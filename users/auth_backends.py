from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from doctor.models import Doctor
from office_assistant.models import OfficeAssistant

from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend

class DoctorOfficeAssistantBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        # First, try to authenticate using the default ModelBackend (superusers, staff)
        user = super().authenticate(request, username=username, password=password, **kwargs)
        if user is not None:
            return user

        # Try to authenticate as Doctor
        try:
            doctor = Doctor.objects.get(username=username)
            if doctor.password and check_password(password, doctor.password):
                user, created = User.objects.get_or_create(username=username)
                return user
        except Doctor.DoesNotExist:
            pass

        # Try to authenticate as OfficeAssistant
        try:
            assistant = OfficeAssistant.objects.get(username=username)
            if assistant.password and check_password(password, assistant.password):
                user, created = User.objects.get_or_create(username=username)
                return user
        except OfficeAssistant.DoesNotExist:
            pass

        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
