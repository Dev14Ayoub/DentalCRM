# dental/urls.py
from django.urls import path
from dental.views import PatientListView, PatientDetailView, appointment_calendar, AppointmentDetailView
from django.contrib.auth import views as auth_views
from rest_framework.routers import DefaultRouter
from .api import AppointmentViewSet

router = DefaultRouter()
router.register(r'appointments', AppointmentViewSet, basename='appointment')

urlpatterns = [
    path('patients/', PatientListView.as_view(), name='patient_list'),
    path('patients/<int:pk>/', PatientDetailView.as_view(), name='patient_detail'),
    path('appointments/<int:pk>/', AppointmentDetailView.as_view(), name='appointment_detail'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('calendar/', appointment_calendar, name='appointment_calendar'),
] + router.urls
