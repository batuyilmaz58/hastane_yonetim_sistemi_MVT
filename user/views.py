from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .models import CustomUser
from .forms import UserLoginForm, UserRegisterForm
from doctor.models import Doctor
import logging

logger = logging.getLogger(__name__)


class UserLoginView(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True
    
    
    def get_success_url(self):
        logger.info(f"User '{self.request.user.username}' logged in successfully.")
        return reverse_lazy("dashboard")

class UserLogoutView(View):
    def get(self, request):
        logout(request)
        logger.info(f"User '{request.user.username}' logged out successfully.")
        messages.success(request, "Başarıyla çıkış yaptınız.")
        return redirect("login")

    def post(self, request):
        logout(request)
        logger.info(f"User '{request.user.username}' logged out successfully.")
        messages.success(request, "Başarıyla çıkış yaptınız.")
        return redirect("login")

class UserRegisterView(CreateView):
    model = CustomUser
    form_class = UserRegisterForm
    template_name = 'register.html'
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()

        if user.role == 'DOCTOR':
            Doctor.objects.create(
                user=user,
                license_number=form.cleaned_data['license_number'],
                specialization=form.cleaned_data['specialization']
            )
            logger.info(f"New doctor registered: '{user.username}' (ID: {user.id})")
        else:
            logger.info(f"New user registered: '{user.username}' (ID: {user.id})")

        messages.success(self.request, "Kayıt başarıyla tamamlandı. Lütfen giriş yapınız.")
        return redirect(self.success_url)

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from patient.models import Patient
        from appointment.models import Appointment
        from doctor.models import Doctor

        context['total_patients'] = Patient.objects.count()
        context['total_doctors'] = Doctor.objects.count()
        context['total_appointments'] = Appointment.objects.count()
        context['scheduled_appointments'] = Appointment.objects.filter(status='SCHEDULED').count()
        return context
