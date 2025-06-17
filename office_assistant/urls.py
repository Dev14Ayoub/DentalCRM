from django.urls import path
from .views import AssistantListView, AssistantCreateView, AssistantUpdateView, AssistantDetailView, AssistantDeleteView, NoteListView, AppointmentReminderListView, OfficeAssistantCreateView

app_name = 'office_assistant'

urlpatterns = [
    path('assistants/', AssistantListView.as_view(), name='assistant_list'),
    path('assistants/create/', OfficeAssistantCreateView.as_view(), name='assistant_create'),
    path('assistants/<int:pk>/', AssistantDetailView.as_view(), name='assistant_detail'),
    path('assistants/<int:pk>/update/', AssistantUpdateView.as_view(), name='assistant_update'),
    path('assistants/<int:pk>/delete/', AssistantDeleteView.as_view(), name='assistant_delete'),
    path('officeassistants/create/', OfficeAssistantCreateView.as_view(), name='officeassistant_create'),
    path('notes/', NoteListView.as_view(), name='note_list'),
    path('reminders/', AppointmentReminderListView.as_view(), name='reminder_list'),
]
