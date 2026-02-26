from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser
from doctor.models import Doctor


class DoctorInline(admin.TabularInline):
    model = Doctor
    extra = 0
    fields = ('license_number', 'specialization', 'created_at')
    readonly_fields = ('created_at',)

    def has_add_permission(self, request, obj=None):
        # Only show if user is already a doctor
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'phone')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Status', {'fields': ('role', 'created_at')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    readonly_fields = ('created_at', 'date_joined', 'last_login')
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'phone', 'is_active')
    list_filter = ('role', 'is_active', 'is_staff', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'phone')
    ordering = ('-date_joined',)

    def get_inlines(self, request, obj):
        if obj and obj.role == 'DOCTOR':
            return [DoctorInline]
        return []

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        if change:  # Existing user
            try:
                old_obj = CustomUser.objects.get(pk=obj.pk)
                old_role = old_obj.role
            except CustomUser.DoesNotExist:
                old_role = None

            new_role = obj.role

            # Rol DOCTOR'dan başka bir rolle dönüştürüldüyse, Doctor kaydını sil
            if old_role == 'DOCTOR' and new_role != 'DOCTOR':
                Doctor.objects.filter(user=obj).delete()
                self.message_user(request, f"{obj.username} artık doktor değildir. Doctor kaydı silinmiştir.")

            # Rol başka bir rollen DOCTOR'a dönüştürüldüyse, uyarı ver
            elif old_role != 'DOCTOR' and new_role == 'DOCTOR':
                if not Doctor.objects.filter(user=obj).exists():
                    self.message_user(
                        request,
                        f"{obj.username} doktor rolüne dönüştürüldü. Lütfen doktor bilgilerini (Lisans Numarası, Uzmanlık) ekleyin.",
                        level=admin.messages.WARNING
                    )
