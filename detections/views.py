"""Detections views."""
# Django
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView, ListView

# Models
from detections.models import Detection


class IndexView(LoginRequiredMixin, ListView):
    """Return Index."""
    template_name = 'detections/index.html'
    model = Detection
    context_object_name = 'detetions'

class AllDetectionsView(LoginRequiredMixin, ListView):
    """Return detections."""
    template_name = 'detections/all-detections.html'
    model = Detection
    ordering = ('-created',)
    paginate_by = 5
    context_object_name = 'detections'

class DetectionDetailView(LoginRequiredMixin, DetailView):
    """Detection detail view."""
    template_name = 'detections/detail.html'
    slug_field = 'name'
    slug_url_kwarg = 'name'
    model = Detection
    context_object_name = 'detection'
