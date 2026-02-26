from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Doctor

class DoctorListView(LoginRequiredMixin, ListView):
    model = Doctor
    template_name = 'doctor_list.html'
    context_object_name = 'doctors'
    ordering = ['user__last_name']

class DoctorDetailView(LoginRequiredMixin, DetailView):
    model = Doctor
    template_name = 'doctor_detail.html'
