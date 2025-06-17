from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from .models import (
    Patient, Insurance, TreatmentPlan, Appointment, 
    AppointmentPhoto, PatientNote, Payment, Prescription
)
from .forms import (
    PatientForm, PatientCreateForm, PatientUpdateForm, TreatmentPlanForm,
    AppointmentForm, AppointmentPhotoForm, PatientNoteForm, PaymentForm,
    PrescriptionForm, InsuranceForm, QuickAppointmentForm
)
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.http import JsonResponse, HttpResponseForbidden, HttpResponseRedirect
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Sum, Count, Q
from datetime import date, timedelta
from django.core.exceptions import PermissionDenied

class PatientListView(LoginRequiredMixin, ListView):
    model = Patient
    template_name = 'patient/list.html'
    context_object_name = 'patients'
    paginate_by = 10
    login_url = 'users:login'

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if user.groups.filter(name='Lead').exists():
            raise PermissionDenied("You do not have permission to view this page.")
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        user = self.request.user
        # If user is superuser or staff, show all patients of the clinic
        if user.is_superuser or user.is_staff:
            queryset = Patient.objects.filter(clinic=user.clinic).order_by('-created_at')
        elif hasattr(user, 'doctor'):
            # Doctor sees patients created by them or assigned as primary doctor
            queryset = Patient.objects.filter(
                Q(created_by=user) | Q(primary_doctor__user=user)
            ).order_by('-created_at')
        else:
            queryset = Patient.objects.filter(created_by=user).order_by('-created_at')

        search_query = self.request.GET.get('search', '').strip()

        if search_query:
            queryset = queryset.filter(
                Q(first_name__icontains=search_query) |
                Q(last_name__icontains=search_query) |
                Q(phone__icontains=search_query) |
                Q(email__icontains=search_query)
            )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add dashboard statistics
        context['total_patients'] = Patient.objects.filter(created_by=self.request.user).count()
        context['upcoming_appointments'] = Appointment.objects.filter(
            patient__created_by=self.request.user,
            date__gte=date.today(),
            status__in=['scheduled', 'confirmed']
        ).count()
        return context

class PatientCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Patient
    form_class = PatientCreateForm
    template_name = 'patient/create.html'
    success_url = reverse_lazy('patient:list')
    permission_required = 'patient.add_patient'

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.is_staff:
            return Patient.objects.filter(clinic=user.clinic)
        elif hasattr(user, 'doctor'):
            # Doctor sees patients created by them or assigned as primary doctor
            return Patient.objects.filter(
                Q(created_by=user) | Q(primary_doctor__user=user)
            )
        else:
            return Patient.objects.filter(created_by=user)

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, 'Patient created successfully!')
        return super().form_valid(form)

class PatientUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Patient
    form_class = PatientUpdateForm
    template_name = 'patient/update.html'
    success_url = reverse_lazy('patient:list')
    permission_required = 'patient.change_patient'

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if user.groups.filter(name='Lead').exists():
            raise PermissionDenied("You do not have permission to access this page.")
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.is_staff:
            return Patient.objects.filter(clinic=user.clinic)
        elif hasattr(user, 'doctor'):
            return Patient.objects.filter(created_by=user)
        else:
            return Patient.objects.filter(created_by=user)

    def form_valid(self, form):
        messages.success(self.request, 'Patient updated successfully!')
        return super().form_valid(form)

class PatientDetailView(LoginRequiredMixin, DetailView):
    model = Patient
    template_name = 'patient/detail.html'
    context_object_name = 'patient'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        patient = self.get_object()

        user = self.request.user
        # Check if user is office assistant
        is_office_assistant = user.groups.filter(name='Office Assistant').exists()

        # Get all related data
        context['treatment_plans'] = patient.treatment_plans.all().order_by('-created_at')
        if is_office_assistant:
            # Office assistant sees only appointment dates (past appointments)
            context['appointments'] = patient.appointments.filter(date__lt=date.today()).order_by('-date')
        else:
            context['appointments'] = patient.appointments.prefetch_related('photos', 'patient_notes').order_by('-date', '-time')
        context['notes'] = patient.notes.order_by('-created_at')
        context['payments'] = patient.payments.order_by('-payment_date')
        context['prescriptions'] = patient.prescriptions.order_by('-prescribed_date')
        context['insurance_info'] = patient.insurance_info.all()

        # Add forms for quick actions
        context['treatment_plan_form'] = TreatmentPlanForm(patient=patient)
        context['appointment_form'] = AppointmentForm(patient=patient)
        context['payment_form'] = PaymentForm(patient=patient)
        context['prescription_form'] = PrescriptionForm(patient=patient)
        context['insurance_form'] = InsuranceForm(patient=patient)
        context['quick_appointment_form'] = QuickAppointmentForm()

        # Calculate financial summary
        total_treatment_cost = patient.treatment_plans.aggregate(
            total=Sum('estimated_cost')
        )['total'] or 0
        total_payments = patient.payments.aggregate(
            total=Sum('amount')
        )['total'] or 0
        context['financial_summary'] = {
            'total_treatment_cost': total_treatment_cost,
            'total_payments': total_payments,
            'outstanding_balance': total_treatment_cost - total_payments
        }

        return context

class PatientDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Patient
    template_name = 'patient/delete.html'
    success_url = reverse_lazy('patient:list')
    context_object_name = 'patient'
    permission_required = 'patient.delete_patient'

    def get_queryset(self):
        if self.request.user.is_superuser or self.request.user.is_staff:
            return Patient.objects.filter(clinic=self.request.user.clinic)
        else:
            return Patient.objects.filter(created_by=self.request.user)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Patient deleted successfully!')
        return super().delete(request, *args, **kwargs)

# Treatment Plan Views
@login_required
def create_treatment_plan(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    if request.method == 'POST':
        form = TreatmentPlanForm(request.POST, patient=patient, doctor=request.user.doctor if hasattr(request.user, 'doctor') else None)
        if form.is_valid():
            treatment_plan = form.save()
            messages.success(request, 'Treatment plan created successfully!')
        else:
            messages.error(request, 'Failed to create treatment plan. Please check the form.')
    return redirect('patient:detail', pk=patient.id)

# Appointment Views
@login_required
def create_appointment(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    if request.method == 'POST':
        # Handle quick appointment form
        if 'quick_appointment' in request.POST:
            form = QuickAppointmentForm(request.POST, request.FILES)
            if form.is_valid():
                # Create appointment
                appointment = Appointment.objects.create(
                    patient=patient,
                    date=form.cleaned_data['date'],
                    time='09:00',  # Default time
                    doctor=patient.primary_doctor,
                )
                
                # Handle photos
                photos = request.FILES.getlist('photos')
                for photo in photos:
                    AppointmentPhoto.objects.create(
                        appointment=appointment,
                        photo=photo
                    )
                
                # Handle note
                note_text = form.cleaned_data.get('note')
                if note_text:
                    PatientNote.objects.create(
                        patient=patient,
                        appointment=appointment,
                        note=note_text,
                        doctor=patient.primary_doctor
                    )
                
                messages.success(request, 'Appointment history added successfully!')
            else:
                messages.error(request, 'Failed to add appointment history. Please check the form.')
        else:
            # Handle regular appointment form
            form = AppointmentForm(request.POST, patient=patient, doctor=request.user.doctor if hasattr(request.user, 'doctor') else None)
            if form.is_valid():
                appointment = form.save()
                messages.success(request, 'Appointment scheduled successfully!')
            else:
                messages.error(request, 'Failed to schedule appointment. Please check the form.')
    
    return redirect('patient:detail', pk=patient.id)

# Payment Views
@login_required
def create_payment(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    if request.method == 'POST':
        form = PaymentForm(request.POST, patient=patient)
        if form.is_valid():
            payment = form.save()
            messages.success(request, 'Payment recorded successfully!')
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': True})
            else:
                return redirect('patient:detail', pk=patient.id)
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'error': 'Invalid form data'})
            else:
                messages.error(request, 'Failed to record payment. Please check the form.')
                return redirect('patient:detail', pk=patient.id)
    else:
        return redirect('patient:detail', pk=patient.id)

# Prescription Views
@login_required
def create_prescription(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    if request.method == 'POST':
        form = PrescriptionForm(
            request.POST, 
            patient=patient, 
            doctor=request.user.doctor if hasattr(request.user, 'doctor') else None
        )
        if form.is_valid():
            prescription = form.save()
            messages.success(request, 'Prescription created successfully!')
        else:
            messages.error(request, 'Failed to create prescription. Please check the form.')
    return redirect('patient:detail', pk=patient.id)

# Insurance Views
@login_required
def create_insurance(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    if request.method == 'POST':
        form = InsuranceForm(request.POST, patient=patient)
        if form.is_valid():
            insurance = form.save()
            messages.success(request, 'Insurance information added successfully!')
        else:
            messages.error(request, 'Failed to add insurance information. Please check the form.')
    return redirect('patient:detail', pk=patient.id)

# Photo and Note Management
@login_required
def add_appointment_photo(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    if request.method == 'POST':
        form = AppointmentPhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.appointment = appointment
            photo.save()
            messages.success(request, 'Photo added successfully!')
        else:
            messages.error(request, 'Failed to add photo. Please check the form.')
    return redirect('patient:detail', pk=appointment.patient.id)

@login_required
def add_patient_note(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    if request.method == 'POST':
        form = PatientNoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.patient = patient
            note.doctor = request.user.doctor if hasattr(request.user, 'doctor') else None
            note.save()
            messages.success(request, 'Note added successfully!')
        else:
            messages.error(request, 'Failed to add note. Please check the form.')
    return redirect('patient:detail', pk=patient.id)


# AJAX Views for dynamic updates
@login_required
@require_POST
def delete_appointment_photo(request, photo_id):
    photo = get_object_or_404(AppointmentPhoto, id=photo_id)
    if photo.appointment.patient.created_by != request.user:
        return HttpResponseForbidden("You do not have permission to delete this photo.")
    photo.delete()
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True})
    return redirect(request.META.get('HTTP_REFERER', 'patient:list'))

@login_required
@require_POST
def update_treatment_plan_status(request, plan_id):
    treatment_plan = get_object_or_404(TreatmentPlan, id=plan_id)
    # Check if the user has permission to update the treatment plan
    if treatment_plan.patient.created_by != request.user and (not hasattr(request.user, 'doctor') or treatment_plan.doctor != request.user.doctor):
        return HttpResponseForbidden("You do not have permission to update this treatment plan.")
    new_status = request.POST.get('status')
    if new_status not in dict(TreatmentPlan.STATUS_CHOICES):
        messages.error(request, "Invalid status value.")
        return redirect('patient:detail', pk=treatment_plan.patient.id)
    treatment_plan.status = new_status
    treatment_plan.save()
    messages.success(request, "Treatment plan status updated successfully.")
    return redirect('patient:detail', pk=treatment_plan.patient.id)

@login_required
@require_POST
def update_appointment_status(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    # Check if the user has permission to update the appointment
    if appointment.patient.created_by != request.user and (not hasattr(request.user, 'doctor') or appointment.doctor != request.user.doctor):
        return HttpResponseForbidden("You do not have permission to update this appointment.")
    new_status = request.POST.get('status')
    if new_status not in dict(Appointment.STATUS_CHOICES):
        messages.error(request, "Invalid status value.")
        return redirect('patient:detail', pk=appointment.patient.id)
    appointment.status = new_status
    appointment.save()
    messages.success(request, "Appointment status updated successfully.")
    return redirect('patient:detail', pk=appointment.patient.id)

@login_required
def patient_dashboard(request):
    """Dashboard view with statistics and recent activity"""
    patients = Patient.objects.filter(created_by=request.user)
    
    context = {
        'total_patients': patients.count(),
        'recent_patients': patients.order_by('-created_at')[:5],
        'upcoming_appointments': Appointment.objects.filter(
            patient__created_by=request.user,
            date__gte=date.today(),
            status__in=['scheduled', 'confirmed']
        ).order_by('date', 'time')[:10],
        'recent_payments': Payment.objects.filter(
            patient__created_by=request.user
        ).order_by('-payment_date')[:5],
        'total_revenue': Payment.objects.filter(
            patient__created_by=request.user
        ).aggregate(total=Sum('amount'))['total'] or 0,
    }
    
    return render(request, 'patient/dashboard.html', context)