from django.contrib import admin
from .models import Doctor, DoctorSchedule


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('get_name', 'license_number', 'specialization', 'get_email', 'created_at')
    list_filter = ('specialization', 'created_at')
    search_fields = ('license_number', 'user__first_name', 'user__last_name', 'user__email')
    readonly_fields = ('created_at',)
    fieldsets = (
        ('Professional Info', {'fields': ('user', 'license_number', 'specialization')}),
        ('Dates', {'fields': ('created_at',)}),
    )

    def get_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"
    get_name.short_description = 'Doctor Name'

    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'Email'


@admin.register(DoctorSchedule)
class DoctorScheduleAdmin(admin.ModelAdmin):
    list_display = ('get_doctor_name', 'get_day', 'start_time', 'end_time', 'is_available')
    list_filter = ('day_of_week', 'is_available', 'doctor')
    search_fields = ('doctor__user__first_name', 'doctor__user__last_name')
    fieldsets = (
        ('Schedule Info', {'fields': ('doctor', 'day_of_week', 'start_time', 'end_time')}),
        ('Status', {'fields': ('is_available',)}),
    )

    def get_doctor_name(self, obj):
        return f"{obj.doctor.user.first_name} {obj.doctor.user.last_name}"
    get_doctor_name.short_description = 'Doctor'

    def get_day(self, obj):
        return obj.get_day_of_week_display()
    get_day.short_description = 'Day'
