"""Detections views."""
# Django
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView, ListView

# Models
from detections.models import Detection



class DetectionIndexView(LoginRequiredMixin, ListView):
    """Return all published detections."""

    template_name = 'index.html'
    model = Detection
    context_object_name = 'detetions'
