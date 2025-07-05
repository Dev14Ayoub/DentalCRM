from django.contrib import admin
from .models import (
    Patient, Insurance, TreatmentPlan, Appointment, 
    AppointmentPhoto, PatientNote, Payment, Prescription
)

class InsuranceInline(admin.TabularInline):
    model = Insurance
    extra = 0
    readonly_fields = ('created_at', 'updated_at')

class TreatmentPlanInline(admin.TabularInline):
    model = TreatmentPlan
    extra = 0
    readonly_fields = ('created_at', 'updated_at')
    fields = ('title', 'status', 'estimated_cost', 'patient_responsibility')

class AppointmentInline(admin.TabularInline):
    model = Appointment
    extra = 0
    readonly_fields = ('created_at', 'updated_at')
    fields = ('date', 'time', 'status', 'doctor')

class PatientNoteInline(admin.TabularInline):
    model = PatientNote
    extra = 0
    readonly_fields = ('created_at',)
    fields = ('note', 'doctor', 'appointment')

class PaymentInline(admin.TabularInline):
    model = Payment
    extra = 0
    readonly_fields = ('payment_date',)
    fields = ('amount', 'payment_method', 'treatment_plan')

class PrescriptionInline(admin.TabularInline):
    model = Prescription
    extra = 0
    readonly_fields = ('prescribed_date',)
    fields = ('medication', 'dosage', 'doctor', 'valid_until')

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email', 'phone', 'primary_doctor', 'created_at')
    list_filter = ('gender', 'primary_doctor', 'created_at')
    search_fields = ('id', 'first_name', 'last_name', 'email', 'phone')
    readonly_fields = ('id', 'created_at', 'updated_at', 'age')
    ordering = ('-created_at',)
    inlines = [InsuranceInline, TreatmentPlanInline, AppointmentInline, PatientNoteInline, PaymentInline, PrescriptionInline]
    
    fieldsets = (
        ('Patient Information', {
            'fields': ('id', 'first_name', 'last_name', 'date_of_birth', 'age', 'gender')
        }),
        ('Contact Information', {
            'fields': ('email', 'phone', 'address')
        }),
        ('Medical Information', {
            'fields': ('medical_history', 'primary_doctor')
        }),
        ('Management', {
            'fields': ('created_by',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

class AppointmentPhotoInline(admin.TabularInline):
    model = AppointmentPhoto
    extra = 0
    readonly_fields = ('uploaded_at',)

class AppointmentNoteInline(admin.TabularInline):
    model = PatientNote
    extra = 0
    readonly_fields = ('created_at',)
    fk_name = 'appointment'

class AppointmentPaymentInline(admin.TabularInline):
    model = Payment
    extra = 0
    readonly_fields = ('payment_date',)
    fk_name = 'appointment'

class AppointmentPrescriptionInline(admin.TabularInline):
    model = Prescription
    extra = 0
    readonly_fields = ('prescribed_date',)
    fk_name = 'appointment'

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'date', 'time', 'status', 'treatment_plan')
    list_filter = ('status', 'date', 'doctor', 'treatment_plan')
    search_fields = ('patient__first_name', 'patient__last_name', 'patient__id')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [AppointmentPhotoInline, AppointmentNoteInline, AppointmentPaymentInline, AppointmentPrescriptionInline]
    
    fieldsets = (
        ('Appointment Details', {
            'fields': ('patient', 'doctor', 'treatment_plan')
        }),
        ('Schedule', {
            'fields': ('date', 'time', 'duration', 'status')
        }),
        ('Notes', {
            'fields': ('appointment_notes',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(TreatmentPlan)
class TreatmentPlanAdmin(admin.ModelAdmin):
    list_display = ('title', 'patient', 'doctor', 'status', 'estimated_cost', 'patient_responsibility')
    list_filter = ('status', 'doctor', 'created_at')
    search_fields = ('title', 'patient__first_name', 'patient__last_name')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Treatment Information', {
            'fields': ('patient', 'doctor', 'title', 'description')
        }),
        ('Financial Details', {
            'fields': ('estimated_cost', 'insurance_coverage', 'patient_responsibility')
        }),
        ('Timeline', {
            'fields': ('status', 'start_date', 'end_date')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def save_model(self, request, obj, form, change):
        obj.calculate_patient_responsibility()
        super().save_model(request, obj, form, change)

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'amount', 'payment_method', 'payment_date')
    list_filter = ('payment_method', 'payment_date')
    search_fields = ('patient__first_name', 'patient__last_name', 'transaction_id')
    readonly_fields = ('payment_date',)
    
    fieldsets = (
        ('Payment Information', {
            'fields': ('patient', 'treatment_plan', 'appointment')
        }),
        ('Transaction Details', {
            'fields': ('amount', 'payment_method', 'transaction_id')
        }),
        ('Additional Information', {
            'fields': ('notes', 'payment_date')
        }),
    )

@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ('patient', 'medication', 'doctor', 'prescribed_date', 'valid_until')
    list_filter = ('doctor', 'prescribed_date', 'valid_until')
    search_fields = ('patient__first_name', 'patient__last_name', 'medication')
    readonly_fields = ('prescribed_date',)
    
    fieldsets = (
        ('Prescription Information', {
            'fields': ('patient', 'doctor', 'appointment')
        }),
        ('Medication Details', {
            'fields': ('medication', 'dosage', 'instructions')
        }),
        ('Validity', {
            'fields': ('prescribed_date', 'valid_until', 'notes')
        }),
    )

@admin.register(Insurance)
class InsuranceAdmin(admin.ModelAdmin):
    list_display = ('patient', 'provider', 'policy_number', 'expiry_date')
    list_filter = ('provider', 'expiry_date')
    search_fields = ('patient__first_name', 'patient__last_name', 'provider', 'policy_number')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(AppointmentPhoto)
class AppointmentPhotoAdmin(admin.ModelAdmin):
    list_display = ('appointment', 'caption', 'uploaded_at')
    list_filter = ('uploaded_at',)
    search_fields = ('appointment__patient__first_name', 'appointment__patient__last_name', 'caption')
    readonly_fields = ('uploaded_at',)

@admin.register(PatientNote)
class PatientNoteAdmin(admin.ModelAdmin):
    list_display = ('patient', 'appointment', 'doctor', 'created_at')
    list_filter = ('created_at', 'doctor')
    search_fields = ('patient__first_name', 'patient__last_name', 'note')
    readonly_fields = ('created_at',)
