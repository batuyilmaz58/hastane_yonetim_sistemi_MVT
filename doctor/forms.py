from django import forms
from .models import Doctor, DoctorSchedule


class DoctorForm(forms.ModelForm):
    first_name = forms.CharField(max_length=100, label="Adı", widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Adı'
    }))
    last_name = forms.CharField(max_length=100, label="Soyadı", widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Soyadı'
    }))

    class Meta:
        model = Doctor
        fields = ['license_number', 'specialization']
        widgets = {
            'license_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Lisans Numarası'
            }),
            'specialization': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Uzmanlık Alanı'
            }),
        }


class DoctorScheduleForm(forms.ModelForm):
    class Meta:
        model = DoctorSchedule
        fields = ['day_of_week', 'start_time', 'end_time', 'is_available']
        widgets = {
            'day_of_week': forms.Select(attrs={
                'class': 'form-select'
            }),
            'start_time': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
            }),
            'end_time': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
            }),
            'is_available': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
