from django.urls import path
from . import views

app_name = 'calendar_app'

urlpatterns = [
    path('appointments/', views.AppointmentListView.as_view(), name='appointment_list'),
    path('appointments/create/', views.AppointmentCreateView.as_view(), name='appointment_create'),
    path('appointments/<int:pk>/update/', views.AppointmentUpdateView.as_view(), name='appointment_update'),
    path('appointments/<int:pk>/delete/', views.AppointmentDeleteView.as_view(), name='appointment_delete'),

    path('availabilities/', views.DoctorAvailabilityListView.as_view(), name='doctoravailability_list'),
    path('availabilities/create/', views.DoctorAvailabilityCreateView.as_view(), name='doctoravailability_create'),
    path('availabilities/<int:pk>/update/', views.DoctorAvailabilityUpdateView.as_view(), name='doctoravailability_update'),
    path('availabilities/<int:pk>/delete/', views.DoctorAvailabilityDeleteView.as_view(), name='doctoravailability_delete'),

    path('calendar/', views.CalendarView.as_view(), name='calendar'),
    path('events/', views.CalendarEventsView.as_view(), name='calendar_events'),
    path('events/<str:event_id>/update/', views.CalendarEventsView.as_view(), name='calendar_event_update'),
]
