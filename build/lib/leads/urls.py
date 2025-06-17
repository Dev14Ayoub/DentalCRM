from django.urls import path
from .views import ConvertLeadView
from . import views

app_name = 'leads'

urlpatterns = [
    path('', views.LeadListView.as_view(), name='list'),
    path('create/', views.LeadCreateView.as_view(), name='create'),
    path('update/<str:pk>/', views.LeadUpdateView.as_view(), name='update'),
    path('delete/<str:pk>/', views.LeadDeleteView.as_view(), name='delete'),
    path('<str:pk>/', views.LeadDetailView.as_view(), name='detail'),
    path('convert/<str:pk>/', ConvertLeadView.as_view(), name='convert'),

]
