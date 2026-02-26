from django import forms
from .models import Appointment
from doctor.models import Doctor


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['patient', 'doctor', 'appointment_date', 'status', 'notes']
        widgets = {
            'patient': forms.Select(attrs={
                'class': 'form-select'
            }),
            'doctor': forms.Select(attrs={
                'class': 'form-select'
            }),
            'appointment_date': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'status': forms.Select(attrs={
                'class': 'form-select'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Notlar'
            }),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user and user.role == 'DOCTOR':
            # Doktor sadece kendisini görebilir
            try:
                doctor = Doctor.objects.get(user=user)
                self.fields['doctor'].queryset = Doctor.objects.filter(user=user)
            except Doctor.DoesNotExist:
                self.fields['doctor'].queryset = Doctor.objects.none()
        else:
            # Sekreter tüm doktorları görebilir
            self.fields['doctor'].queryset = Doctor.objects.all()
