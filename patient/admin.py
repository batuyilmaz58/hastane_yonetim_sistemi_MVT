from django.contrib import admin
from .models import Patient, MedicalRecord


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'national_id', 'date_of_birth', 'gender', 'phone', 'blood_type', 'created_at')
    list_filter = ('gender', 'created_at', 'date_of_birth', 'blood_type')
    search_fields = ('first_name', 'last_name', 'national_id', 'phone', 'email')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Personal Information', {'fields': ('first_name', 'last_name', 'national_id', 'email')}),
        ('Contact Info', {'fields': ('phone', 'address')}),
        ('Medical Info', {'fields': ('date_of_birth', 'gender', 'blood_type', 'allergies')}),
        ('Dates', {'fields': ('created_at', 'updated_at')}),
    )

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    get_full_name.short_description = 'Patient Name'


@admin.register(MedicalRecord)
class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = ('get_patient_name', 'get_doctor_name', 'diagnosis', 'visit_date', 'created_at')
    list_filter = ('visit_date', 'created_at', 'diagnosis')
    search_fields = ('patient__first_name', 'patient__last_name', 'doctor__first_name', 'doctor__last_name', 'diagnosis')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Record Information', {'fields': ('patient', 'doctor', 'visit_date')}),
        ('Medical Details', {'fields': ('diagnosis', 'treatment', 'prescription')}),
        ('Notes', {'fields': ('notes',)}),
        ('Dates', {'fields': ('created_at', 'updated_at')}),
    )

    def get_patient_name(self, obj):
        return f"{obj.patient.first_name} {obj.patient.last_name}"
    get_patient_name.short_description = 'Patient'

    def get_doctor_name(self, obj):
        if obj.doctor:
            return f"{obj.doctor.first_name} {obj.doctor.last_name}"
        return '-'
    get_doctor_name.short_description = 'Doctor'
