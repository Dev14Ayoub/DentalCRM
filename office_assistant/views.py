from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django.urls import reverse_lazy
from .models import  Note, AppointmentReminder, OfficeAssistant
from .forms import NoteForm, AppointmentReminderForm, OfficeAssistantForm

class AssistantListView(ListView):
    model = OfficeAssistant
    template_name = 'office_assistant/list.html'
    context_object_name = 'assistants'

class AssistantCreateView(CreateView):
    model = OfficeAssistant
    form_class = OfficeAssistantForm
    template_name = 'office_assistant/create.html'
    success_url = reverse_lazy('office_assistant:assistant_list')

class AssistantUpdateView(UpdateView):
    model = OfficeAssistant
    form_class = OfficeAssistantForm
    template_name = 'office_assistant/update.html'
    success_url = reverse_lazy('office_assistant:assistant_list')

class AssistantDetailView(DetailView):
    model = OfficeAssistant
    template_name = 'office_assistant/detail.html'
    context_object_name = 'assistant'

class AssistantDeleteView(DeleteView):
    model = OfficeAssistant
    template_name = 'office_assistant/delete.html'
    success_url = reverse_lazy('office_assistant:assistant_list')

class OfficeAssistantCreateView(CreateView):
    model = OfficeAssistant
    form_class = OfficeAssistantForm
    template_name = 'office_assistant/create.html'
    success_url = reverse_lazy('office_assistant:assistant_list')

class NoteListView(ListView):
    model = Note
    template_name = 'office_assistant/note_list.html'
    context_object_name = 'notes'

class NoteCreateView(CreateView):
    model = Note
    form_class = NoteForm
    template_name = 'office_assistant/note_form.html'
    success_url = reverse_lazy('office_assistant:note_list')

class NoteUpdateView(UpdateView):
    model = Note
    form_class = NoteForm
    template_name = 'office_assistant/note_form.html'
    success_url = reverse_lazy('office_assistant:note_list')

class NoteDetailView(DetailView):
    model = Note
    template_name = 'office_assistant/note_detail.html'
    context_object_name = 'note'

class NoteDeleteView(DeleteView):
    model = Note
    template_name = 'office_assistant/note_confirm_delete.html'
    success_url = reverse_lazy('office_assistant:note_list')

class AppointmentReminderListView(ListView):
    model = AppointmentReminder
    template_name = 'office_assistant/appointmentreminder_list.html'
    context_object_name = 'reminders'

class AppointmentReminderCreateView(CreateView):
    model = AppointmentReminder
    form_class = AppointmentReminderForm
    template_name = 'office_assistant/appointmentreminder_form.html'
    success_url = reverse_lazy('office_assistant:appointmentreminder_list')

class AppointmentReminderUpdateView(UpdateView):
    model = AppointmentReminder
    form_class = AppointmentReminderForm
    template_name = 'office_assistant/appointmentreminder_form.html'
    success_url = reverse_lazy('office_assistant:appointmentreminder_list')

class AppointmentReminderDetailView(DetailView):
    model = AppointmentReminder
    template_name = 'office_assistant/appointmentreminder_detail.html'
    context_object_name = 'reminder'

class AppointmentReminderDeleteView(DeleteView):
    model = AppointmentReminder
    template_name = 'office_assistant/appointmentreminder_confirm_delete.html'
    success_url = reverse_lazy('office_assistant:appointmentreminder_list')
