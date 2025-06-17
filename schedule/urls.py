app_name = 'schedule'

from rest_framework.routers import DefaultRouter
from django.urls import path, include
from schedule.views.api import AppointmentViewSet
from schedule.views.schedule_view import ScheduleView, MarkProcedureDoneView
from schedule.views.custom_schedule_view import CustomScheduleView
from schedule.views.confirmation_view import AppointmentConfirmationView as ConfirmationView

router = DefaultRouter()
router.register(r'schedule-api', AppointmentViewSet, basename='schedule-api')

from schedule.views.appointment_views import AvailableAppointmentTimes, AvailableAppointmentDates

urlpatterns = [
    path('', ScheduleView.as_view(), name='schedule'),
    path('custom/', CustomScheduleView.as_view(), name='custom'),
    path('confirm/<str:token>/', ConfirmationView.as_view(), name='confirm'),
    path('times/', AvailableAppointmentTimes.as_view(), name='times'),
    path('dates/', AvailableAppointmentDates.as_view(), name='dates'),
    path('mark_done/<int:appointment_id>/', MarkProcedureDoneView.as_view(), name='mark_procedure_done'),
    path('', include(router.urls)),
]

# Include schedule API URLs in the schedule app's urls.py
# No need to modify config/urls.py for schedule API
