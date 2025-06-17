from django.urls import path
from . import views

app_name = 'patient'

urlpatterns = [
    path('', views.PatientListView.as_view(), name='list'),
    path('create/', views.PatientCreateView.as_view(), name='create'),
    path('update/<str:pk>/', views.PatientUpdateView.as_view(), name='update'),
    path('delete/<str:pk>/', views.PatientDeleteView.as_view(), name='delete'),
    path('<str:pk>/', views.PatientDetailView.as_view(), name='detail'),
]