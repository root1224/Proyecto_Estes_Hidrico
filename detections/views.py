"""Detections views."""
# Django
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView, ListView

# Models
from detections.models import Detection


class IndexView(LoginRequiredMixin, ListView):
    """Return Index."""
    template_name = 'index.html'
    model = Detection
    context_object_name = 'detetions'

class DetectionIndexView(LoginRequiredMixin, ListView):
    """Return detections."""
    template_name = 'icons.html'
    model = Detection
    context_object_name = 'detetions'
