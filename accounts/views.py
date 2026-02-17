from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView

from accounts.models import User
from tour.models import TourBooking
from .forms import UserRegisterForm, UserLoginForm,UserProfileForm
from django.contrib import messages


class UserRegisterView(CreateView):
    form_class = UserRegisterForm
    template_name = "./accounts/register.html"
    success_url = reverse_lazy("accounts:login")


class UserLoginView(LoginView):
    form_class = UserLoginForm
    template_name = "./accounts/login.html"


class UserLogoutView(LogoutView):
    next_page = reverse_lazy("accounts:login")


class ProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = './accounts/profile.html'
    success_url = reverse_lazy('accounts:profile')

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, "اطلاعات پروفایل با موفقیت بروزرسانی شد.")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["bookings"] = TourBooking.objects.filter(
            user=self.request.user
        ).select_related("tour", "tour_date").order_by("-created_at")
        return context