from django.shortcuts import render, redirect
from django.views.generic import DeleteView, ListView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .models import Appointment
from .forms import AppointmentForm
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied
import logging

logger  = logging.getLogger(__name__)

class AppointmentListView(LoginRequiredMixin, ListView):
    model = Appointment
    template_name = 'appointment_list.html'
    context_object_name = 'appointments'
    ordering = ['-appointment_date']

class AppointmentCreateView(LoginRequiredMixin, CreateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = "appointment_form.html"
    success_url = reverse_lazy("appointment_list")

    def form_valid(self, form):
        try:
            response  = super().form_valid(form)
            messages.success(self.request, "Randevu başarıyla oluşturuldu.")
            logger.info(f"Appointment created: {form.instance}")
            return response
        except Exception as e:
            logger.error(f"Error creating appointment: {e}")
            messages.error(self.request, "Randevu oluşturulurken bir hata oluştu.")
            return super().form_invalid(form)

class AppointmentUpdateView(LoginRequiredMixin, UpdateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = "appointment_form.html"
    success_url = reverse_lazy("appointment_list")

    def form_valid(self, form):
        try:
            response = super().form_valid(form)
            messages.success(self.request, "Randevu başarıyla güncellendi.")
            logger.info(f"Appointment updated: {form.instance}")
            return response
        except Exception as e:
            response  = super().form_invalid(form)
            logger.error(f"Error updating appointment: {e}")
            messages.error(self.request, "Randevu güncellenirken bir hata oluştu.")
            return response

class AppointmentDeleteView(LoginRequiredMixin, DeleteView):
    model = Appointment
    template_name = "appointment_delete.html"
    success_url = reverse_lazy("appointment_list")

    def delete(self, request, *args, **kwargs):
        try:
            response = super().delete(request, *args, **kwargs)
            messages.success(request, "Randevu başarıyla silindi.")
            logger.info(f"Appointment deleted: {kwargs['pk']}")
            return response
        except Exception as e:
            logger.error(f"Error deleting appointment: {e}")
            messages.error(request, "Randevu silinirken bir hata oluştu.")
            return redirect("appointment_list")
