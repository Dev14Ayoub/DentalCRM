# dental/api.py
from rest_framework import viewsets, serializers
from .models import Appointment

class AppointmentSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    start = serializers.DateTimeField(source='date_time')
    end = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()

    class Meta:
        model = Appointment
        fields = ['id', 'title', 'start', 'end', 'url', 'status']

    def get_title(self, obj):
        return f"{obj.patient.name} - {obj.purpose}"

    def get_end(self, obj):
        return obj.date_time + timedelta(minutes=obj.duration)

    def get_url(self, obj):
        return reverse('appointment_detail', args=[obj.pk])

class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    filterset_fields = ['date_time', 'doctor', 'status']