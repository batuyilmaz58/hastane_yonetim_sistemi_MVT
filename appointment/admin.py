from django.contrib import admin
from .models import Appointment


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('get_patient_name', 'get_doctor_name', 'appointment_date', 'status', 'created_at')
    list_filter = ('status', 'appointment_date', 'created_at')
    search_fields = ('patient__first_name', 'patient__last_name', 'doctor__user__first_name', 'doctor__user__last_name')
    readonly_fields = ('created_at',)
    fieldsets = (
        ('Appointment Details', {'fields': ('patient', 'doctor', 'appointment_date')}),
        ('Status', {'fields': ('status',)}),
        ('Notes', {'fields': ('notes',)}),
        ('Dates', {'fields': ('created_at',)}),
    )

    def get_patient_name(self, obj):
        return f"{obj.patient.first_name} {obj.patient.last_name}"
    get_patient_name.short_description = 'Patient'

    def get_doctor_name(self, obj):
        return f"{obj.doctor.user.first_name} {obj.doctor.user.last_name}"
    get_doctor_name.short_description = 'Doctor'
