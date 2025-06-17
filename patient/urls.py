from django.urls import path
from . import views
from schedule.views.appointment_views import ToggleAppointmentConfirmation

app_name = 'patient'

urlpatterns = [
    # Patient CRUD
    path('', views.PatientListView.as_view(), name='list'),
    path('dashboard/', views.patient_dashboard, name='dashboard'),
    path('create/', views.PatientCreateView.as_view(), name='create'),
    path('<str:pk>/', views.PatientDetailView.as_view(), name='detail'),
    path('<str:pk>/update/', views.PatientUpdateView.as_view(), name='update'),
    path('<str:pk>/delete/', views.PatientDeleteView.as_view(), name='delete'),
    
    # Treatment Plans
    path('<str:patient_id>/treatment-plan/create/', views.create_treatment_plan, name='create_treatment_plan'),
    path('treatment-plan/<int:plan_id>/update-status/', views.update_treatment_plan_status, name='update_treatment_plan_status'),
    
    # Appointments
    path('<str:patient_id>/appointment/create/', views.create_appointment, name='create_appointment'),
    path('appointment/<int:appointment_id>/update-status/', views.update_appointment_status, name='update_appointment_status'),
    path('appointment/<int:appointment_id>/add-photo/', views.add_appointment_photo, name='add_appointment_photo'),
    
    # Payments
    path('<str:patient_id>/payment/create/', views.create_payment, name='create_payment'),
    
    # Prescriptions
    path('<str:patient_id>/prescription/create/', views.create_prescription, name='create_prescription'),
    
    # Insurance
    path('<str:patient_id>/insurance/create/', views.create_insurance, name='create_insurance'),
    
    # Notes
    path('<str:patient_id>/note/add/', views.add_patient_note, name='add_patient_note'),
    
    # Photo management
    path('photo/<int:photo_id>/delete/', views.delete_appointment_photo, name='delete_appointment_photo'),

    # Appointment confirmation toggle
    path('appointment/<int:pk>/toggle-confirmation/', ToggleAppointmentConfirmation.as_view(), name='toggle_appointment_confirmation'),
]
