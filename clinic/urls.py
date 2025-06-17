from django.urls import path
from .views import ClinicListView

app_name = 'clinic'

urlpatterns = [
    path('', ClinicListView.as_view(), name='clinic_list'),
]
