from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from doctor.models import Doctor
from office_assistant.models import OfficeAssistant

class DoctorOfficeAssistantBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        # Try to authenticate as Doctor
        try:
            doctor = Doctor.objects.get(username=username)
            if doctor.password and doctor.password == password:
                # Create a dummy User object for authentication
                user, created = User.objects.get_or_create(username=username)
                return user
        except Doctor.DoesNotExist:
            pass

        # Try to authenticate as OfficeAssistant
        try:
            assistant = OfficeAssistant.objects.get(username=username)
            if assistant.password and assistant.password == password:
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
