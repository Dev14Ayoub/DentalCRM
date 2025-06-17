# leads/views.py
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from .models import Lead
from .forms import LeadForm
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

class LeadListView(LoginRequiredMixin, ListView):
    model = Lead
    template_name = 'leads/list.html'
    context_object_name = 'leads'
    paginate_by = 10
    login_url = 'users:login'  # Redirect to login page if not authenticated

class LeadCreateView(CreateView):
    model = Lead
    form_class = LeadForm
    template_name = 'leads/create.html'
    success_url = reverse_lazy('leads:list')

class LeadUpdateView(UpdateView):
    model = Lead
    form_class = LeadForm
    template_name = 'leads/update.html'
    success_url = reverse_lazy('leads:list')

class LeadDetailView(DetailView):
    model = Lead
    template_name = 'leads/detail.html'
    context_object_name = 'lead'

class LeadDeleteView(DeleteView):
    model = Lead
    template_name = 'leads/delete.html'
    success_url = reverse_lazy('leads:list')
    context_object_name = 'lead'

class ConvertLeadView(View):
    def post(self, request, pk):
        lead = get_object_or_404(Lead, pk=pk)
        if lead.convert():
            messages.success(request, f"Lead {lead.id} converted successfully!")
        else:
            messages.warning(request, f"Lead {lead.id} was already converted!")
        return redirect('leads:list')
