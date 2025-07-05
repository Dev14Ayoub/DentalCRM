from django import forms
from .models import (
    Patient, Insurance, TreatmentPlan, Appointment, 
    AppointmentPhoto, PatientNote, Payment, Prescription
)

class PatientForm(forms.ModelForm):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    gender = forms.ChoiceField(choices=GENDER_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}))

    class Meta:
        model = Patient
        fields = '__all__'
        exclude = ['created_by', 'id']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={
                'type': 'date', 
                'class': 'form-control',
                'placeholder': 'YYYY-MM-DD'
            }),
            'medical_history': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3,
                'placeholder': 'Medical conditions, allergies, etc.'
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 2,
                'placeholder': 'Full address'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'First Name'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Last Name'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Phone Number'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email Address'
            }),
            'primary_doctor': forms.Select(attrs={'class': 'form-select'}),
        }

class PatientCreateForm(PatientForm):
    pass

class PatientUpdateForm(PatientForm):
    def save(self, commit=True):
        patient = super().save(commit)
        return patient

class TreatmentPlanForm(forms.ModelForm):
    class Meta:
        model = TreatmentPlan
        fields = ['title', 'description', 'estimated_cost', 'insurance_coverage', 'start_date', 'end_date']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'estimated_cost': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'insurance_coverage': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        self.patient = kwargs.pop('patient', None)
        self.doctor = kwargs.pop('doctor', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        treatment_plan = super().save(commit=False)
        if self.patient:
            treatment_plan.patient = self.patient
        if self.doctor:
            treatment_plan.doctor = self.doctor
        if commit:
            treatment_plan.save()
            treatment_plan.calculate_patient_responsibility()
        return treatment_plan

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['date', 'time', 'duration', 'treatment_plan', 'appointment_notes']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'duration': forms.NumberInput(attrs={'class': 'form-control', 'min': '15', 'step': '15'}),
            'treatment_plan': forms.Select(attrs={'class': 'form-select'}),
            'appointment_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        self.patient = kwargs.pop('patient', None)
        self.doctor = kwargs.pop('doctor', None)
        super().__init__(*args, **kwargs)
        
        if self.patient:
            self.fields['treatment_plan'].queryset = TreatmentPlan.objects.filter(patient=self.patient)

    def save(self, commit=True):
        appointment = super().save(commit=False)
        if self.patient:
            appointment.patient = self.patient
        if self.doctor:
            appointment.doctor = self.doctor
        if commit:
            appointment.save()
        return appointment

class AppointmentPhotoForm(forms.ModelForm):
    class Meta:
        model = AppointmentPhoto
        fields = ['photo', 'caption']
        widgets = {
            'photo': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'caption': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Photo caption (optional)'}),
        }

class PatientNoteForm(forms.ModelForm):
    class Meta:
        model = PatientNote
        fields = ['note']
        widgets = {
            'note': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Add your note here...'}),
        }

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['amount', 'payment_method', 'treatment_plan', 'transaction_id', 'notes']
        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'payment_method': forms.Select(attrs={'class': 'form-select'}),
            'treatment_plan': forms.Select(attrs={'class': 'form-select'}),
            'transaction_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Transaction ID (optional)'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Payment notes (optional)'}),
        }

    def __init__(self, *args, **kwargs):
        self.patient = kwargs.pop('patient', None)
        super().__init__(*args, **kwargs)
        
        if self.patient:
            self.fields['treatment_plan'].queryset = TreatmentPlan.objects.filter(patient=self.patient)

    def save(self, commit=True):
        payment = super().save(commit=False)
        if self.patient:
            payment.patient = self.patient
        if commit:
            payment.save()
        return payment

class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ['medication', 'dosage', 'instructions', 'valid_until', 'notes']
        widgets = {
            'medication': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Medication name'}),
            'dosage': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 500mg twice daily'}),
            'instructions': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Instructions for use'}),
            'valid_until': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Additional notes (optional)'}),
        }

    def __init__(self, *args, **kwargs):
        self.patient = kwargs.pop('patient', None)
        self.doctor = kwargs.pop('doctor', None)
        self.appointment = kwargs.pop('appointment', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        prescription = super().save(commit=False)
        if self.patient:
            prescription.patient = self.patient
        if self.doctor:
            prescription.doctor = self.doctor
        if self.appointment:
            prescription.appointment = self.appointment
        if commit:
            prescription.save()
        return prescription

class InsuranceForm(forms.ModelForm):
    class Meta:
        model = Insurance
        fields = ['provider', 'policy_number', 'coverage_details', 'expiry_date']
        widgets = {
            'provider': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Insurance provider name'}),
            'policy_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Policy number'}),
            'coverage_details': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Coverage details'}),
            'expiry_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        self.patient = kwargs.pop('patient', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        insurance = super().save(commit=False)
        if self.patient:
            insurance.patient = self.patient
        if commit:
            insurance.save()
        return insurance

# Quick forms for appointment history
class QuickAppointmentForm(forms.Form):
    date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label='Appointment Date'
    )
    photos = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'multiple': True, 'class': 'form-control', 'accept': 'image/*'}),
        required=False,
        label='Treatment Photos'
    )
    note = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Add notes about this appointment...'}),
        required=False,
        label='Notes'
    )
