from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from .models import Doctor

class DoctorListView(LoginRequiredMixin, ListView):
    model = Doctor
    template_name = 'doctor_list.html'
    context_object_name = 'doctors'
    ordering = ['user__last_name']

    def get_queryset(self):
        user = self.request.user
        if user.role == 'DOCTOR':
            # Doktor sadece kendisini görebilir
            return Doctor.objects.filter(user=user)
        else:
            # Sekreter tüm doktorları görebilir
            return Doctor.objects.all()

class DoctorDetailView(LoginRequiredMixin, DetailView):
    model = Doctor
    template_name = 'doctor_detail.html'

    def get_object(self, queryset=None):
        doctor = super().get_object(queryset)
        user = self.request.user

        # Doktor sadece kendisini görebilir
        if user.role == 'DOCTOR' and doctor.user != user:
            raise PermissionDenied("Bu doktora erişim izniniz yok.")

        return doctor
