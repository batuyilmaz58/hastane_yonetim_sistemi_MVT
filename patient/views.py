from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import DeleteView, ListView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .models import Patient
from .forms import PatientForm
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied
import logging

logger = logging.getLogger(__name__)

class PatientListView(LoginRequiredMixin, ListView):
    model = Patient
    template_name = 'patient_list.html'
    context_object_name = 'patients'
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = Patient.objects.all()
        search = self.request.GET.get('search')
        logger.info(f"PatientListView: search query - {search}")
        if search:
            queryset = queryset.filter(first_name__icontains=search) | queryset.filter(last_name__icontains=search) | queryset.filter(national_id__icontains=search)
        return queryset

class PatientCreateView(LoginRequiredMixin, CreateView):
    model = Patient
    form_class = PatientForm
    template_name = "patient_form.html"
    success_url = reverse_lazy("patient_list")

    def form_valid(self, form):

        try:
            response = super().form_valid(form)
            messages.success(self.request, "Hasta başarıyla oluşturuldu.")
            logger.info(f"Patient created: {form.instance}")
            return response
        except Exception as e:
            logger.error(f"Error creating patient: {e}")
            messages.error(self.request, "Hasta oluşturulurken bir hata oluştu.")
            return super().form_invalid(form)

class PatientUpdateView(LoginRequiredMixin, UpdateView):
    model = Patient
    form_class = PatientForm
    template_name = "patient_form.html"
    success_url = reverse_lazy("patient_list")

    def form_valid(self, form):
        try:
            response = super().form_valid(form)
            messages.success(self.request, "Hasta başarıyla güncellendi.")
            logger.info(f"Patient updated: {form.instance}")
            return response
        except Exception as e:
            response = super().form_invalid(form)
            logger.error(f"Error updating patient: {e}")
            messages.error(self.request, "Hasta güncellenirken bir hata oluştu.")
            return response

class PatientDeleteView(LoginRequiredMixin, DeleteView):
    model = Patient
    template_name = "patient_delete.html"
    success_url = reverse_lazy("patient_list")

    def delete(self, request, *args, **kwargs):
        try:
            response = super().delete(request, *args, **kwargs)
            messages.success(request, "Hasta başarıyla silindi.")
            logger.info(f"Patient deleted: {kwargs['pk']}")
            return response
        except Exception as e:
            logger.error(f"Error deleting patient: {e}")
            messages.error(request, "Hasta silinirken bir hata oluştu.")
            return redirect("patient_list")