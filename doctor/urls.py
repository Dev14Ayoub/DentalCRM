from django.urls import path
from . import views

app_name = 'doctor'

urlpatterns = [
    path('', views.DoctorListView.as_view(), name='list'),
    path('create/', views.DoctorCreateView.as_view(), name='create'),
    path('update/<int:pk>/', views.DoctorUpdateView.as_view(), name='update'),
    path('detail/<int:pk>/', views.DoctorDetailView.as_view(), name='detail'),
    path('delete/<int:pk>/', views.DoctorDeleteView.as_view(), name='delete'),
]