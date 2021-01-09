"""Users views."""

# Django
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import views as auth_views
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, FormView, UpdateView

# Forms
from django import forms
from users.forms import ProfileForm

# Models
from django.contrib.auth.models import User
from users.models import Profile

class LoginView(auth_views.LoginView):
    """Login view."""
    template_name = 'users/login.html'

class LogoutView(LoginRequiredMixin, auth_views.LogoutView):
    """Logout view."""

    template_name = 'users/login.html'


class ProfileDetailView(LoginRequiredMixin, UpdateView):
    """Profile view."""
    template_name = 'users/profile.html'
    model = Profile
    form_class = ProfileForm

    def get_object(self, *args, **kwargs):
        #user = get_object_or_404(User, pk=self.kwargs['pk'])

        # We can also get user object using self.request.user  but that doesnt work
        # for other models.

        return self.request.user.profile

    def get_success_url(self, *args, **kwargs):
        return reverse("users:profile")
