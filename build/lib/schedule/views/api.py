from rest_framework import viewsets, permissions
from rest_framework.pagination import PageNumberPagination
from schedule.models import Appointment
from schedule.serializers import AppointmentSerializer


class AppointmentPagination(PageNumberPagination):
    page_size = 10


class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all().order_by('-id')
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = AppointmentPagination

    def get_queryset(self):
        # Return only appointments of the logged-in user
        user = self.request.user
        qs = self.queryset.filter(user=user)
        print(f"AppointmentViewSet.get_queryset: user={user}, count={qs.count()}")
        return qs
    
    def perform_create(self, serializer):
        # Set the user to the logged-in user, ignore user field in request data
        serializer.save(user=self.request.user)
